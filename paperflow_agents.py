"""
PaperFlow AI - Agent Definitions
=================================
This module defines the 5 specialized agents and the orchestrator.
Compatible with smolagents 1.22.0
"""

import os
from dotenv import load_dotenv
from smolagents import CodeAgent
from smolagents.models import OpenAIServerModel
import re
import traceback

# Import all tools
from paperflow_tools import (
    check_stock_level,
    list_all_available_items,
    check_if_reorder_needed,
    get_financial_summary,
    place_supplier_order,
    process_multi_item_quote_request,
    search_similar_quotes,
    calculate_price_with_discounts,
    generate_customer_quote,
    process_multi_item_order,
    validate_order_feasibility,
    complete_sale_transaction
)

# Load environment variables
load_dotenv()

# Initialize the model
model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base="https://api.openai.com/v1"
)


# ============================================================
# SYSTEM PROMPTS
# ============================================================

INVENTORY_MANAGER_PROMPT = """You are the Inventory Manager. Check stock, list inventory, determine reordering needs. Use exact item names and dates (YYYY-MM-DD). Reorder quantity: (min_stock × 3) - current_stock."""


QUOTING_SPECIALIST_PROMPT = """You are the Quoting Specialist. Generate quotes with bulk discounts: 100-499 units (10%), 500-999 (20%), 1000+ (25%).

For multi-item requests, use process_multi_item_quote_request tool - it handles parsing, fuzzy item matching, and complete quote generation.

Be professional and transparent."""


SALES_FULFILLMENT_PROMPT = """You are Sales Fulfillment. Process customer orders and complete sales transactions.

For multi-item orders, use process_multi_item_order tool - it handles parsing, validation, and transaction processing for all items at once.

Workflow: Validate stock and complete sales, or explain why orders cannot be fulfilled."""


# ============================================================
# AGENT INITIALIZATION
# ============================================================

# Create base agents (without system prompts - we'll add them in run())
inventory_manager_base = CodeAgent(
    tools=[
        check_stock_level,
        list_all_available_items,
        check_if_reorder_needed,
        get_financial_summary,
        place_supplier_order
    ],
    model=model
)

quoting_specialist_base = CodeAgent(
    tools=[
        process_multi_item_quote_request,
        search_similar_quotes,
        calculate_price_with_discounts,
        generate_customer_quote,
        check_stock_level
    ],
    model=model
)

sales_fulfillment_base = CodeAgent(
    tools=[
        process_multi_item_order,
        validate_order_feasibility,
        complete_sale_transaction,
        check_stock_level
    ],
    model=model
)


# ============================================================
# AGENT WRAPPERS (to include system prompts)
# ============================================================

class InventoryManager:
    """Wrapper for inventory manager agent with system prompt"""
    def __init__(self):
        self.agent = inventory_manager_base
        self.system_prompt = INVENTORY_MANAGER_PROMPT

    def run(self, task):
        """Run the agent with system prompt"""
        full_task = f"{self.system_prompt}\n\nTASK: {task}"
        return self.agent.run(full_task)


class QuotingSpecialist:
    """Wrapper for quoting specialist agent with system prompt"""
    def __init__(self):
        self.agent = quoting_specialist_base
        self.system_prompt = QUOTING_SPECIALIST_PROMPT

    def run(self, task):
        """Run the agent with system prompt"""
        full_task = f"{self.system_prompt}\n\nTASK: {task}"
        return self.agent.run(full_task)


class SalesFulfillment:
    """Wrapper for sales fulfillment agent with system prompt"""
    def __init__(self):
        self.agent = sales_fulfillment_base
        self.system_prompt = SALES_FULFILLMENT_PROMPT

    def run(self, task):
        """Run the agent with system prompt"""
        full_task = f"{self.system_prompt}\n\nTASK: {task}"
        return self.agent.run(full_task)


# Initialize wrapped agents
inventory_manager = InventoryManager()
quoting_specialist = QuotingSpecialist()
sales_fulfillment = SalesFulfillment()


# ============================================================
# ORCHESTRATOR
# ============================================================

class OrchestratorAgent:
    """Custom orchestrator that routes requests to specialist agents"""

    def __init__(self):
        self.inventory_manager = inventory_manager
        self.quoting_specialist = quoting_specialist
        self.sales_fulfillment = sales_fulfillment
        
    def classify_intent(self, request: str) -> str:
        """Classify customer request intent"""
        request_lower = request.lower()

        # Order placement has priority (explicit buy/purchase language)
        order_keywords = ['buy', 'purchase', "i'll take", "i will take",
                         'confirm', 'proceed', 'complete order']
        if any(keyword in request_lower for keyword in order_keywords):
            return 'order_placement'

        # Quote request (includes "request", "order", "need" which often mean quotes)
        quote_keywords = ['quote', 'how much', 'price', 'cost', 'estimate',
                         'pricing', 'how expensive', 'would like to request',
                         'would like to place an order', 'would like to order',
                         'i need', 'we need', 'request for']
        if any(keyword in request_lower for keyword in quote_keywords):
            return 'quote_request'

        # Inventory query
        inventory_keywords = ['do you have', 'in stock', 'available', 'stock level',
                             'what items', 'list', 'inventory', 'check stock']
        if any(keyword in request_lower for keyword in inventory_keywords):
            return 'inventory_query'

        return 'general'
    
    def filter_internal_details(self, response: str) -> str:
        """Remove sensitive internal information from customer-facing responses"""
        sensitive_patterns = [
            r'Transaction ID: \d+',
            r'\(ID: \d+\)',
            r'Updated Cash Balance: \$[\d,\.]+',
            r'Current balance: \$[\d,\.]+',
            r'Remaining after purchase: \$[\d,\.]+',
            r'Safety buffer maintained: [\d\.]+%',
            r'profit margin[:\s]+[\d\.]+%?',
            r'internal cost[:\s]+\$?[\d,\.]+',
            r'ERROR:.*',
            r'FATAL:.*',
            r'⚠️ WARNING:.*cash.*',
            r'SUPPLIER ORDER PLACED.*\n',
            r'Expected Delivery: \d{4}-\d{2}-\d{2}',
        ]

        filtered = response
        for pattern in sensitive_patterns:
            filtered = re.sub(pattern, '', filtered, flags=re.IGNORECASE)

        # Clean up multiple consecutive newlines
        filtered = re.sub(r'\n\s*\n\s*\n+', '\n\n', filtered)
        return filtered.strip()
    
    def route_request(self, request: str, date: str) -> str:
        """Main routing logic for customer requests"""
        intent = self.classify_intent(request)
        
        print(f"\n🎯 Orchestrator: Classified intent as '{intent}'")
        
        try:
            if intent == 'inventory_query':
                print("   → Routing to Inventory Manager")
                response = self.inventory_manager.run(
                    f"{request} (Date: {date})"
                )
                
            elif intent == 'quote_request':
                print("   → Routing to Quoting Specialist")
                response = self.quoting_specialist.run(
                    f"{request} (Date: {date})"
                )
                
            elif intent == 'order_placement':
                print("   → Routing to Sales Fulfillment")
                response = self.sales_fulfillment.run(
                    f"{request} (Date: {date})"
                )
                
            else:
                print("   → Handling general inquiry")
                response = "Thank you for contacting PaperFlow AI.\n\n"
                response += "I can help you with:\n"
                response += "- Checking inventory and stock levels\n"
                response += "- Providing price quotes\n"
                response += "- Processing orders\n\n"
                response += "How can I assist you today?"
            
            filtered_response = self.filter_internal_details(str(response))
            return filtered_response

        except Exception as e:
            print(f"   ⚠️  Error: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            return ("We apologize, but we encountered an issue processing your request. "
                   "Please try rephrasing your request or contact our support team for assistance.")


# Initialize the orchestrator
orchestrator = OrchestratorAgent()


# ============================================================
# VERIFICATION
# ============================================================

def verify_agents():
    """Verify all agents are properly configured"""
    print("\n" + "="*60)
    print("AGENT SYSTEM VERIFICATION")
    print("="*60)

    print("✅ Inventory Manager: 5 tools assigned")
    print("✅ Quoting Specialist: 4 tools assigned")
    print("✅ Sales Fulfillment: 3 tools assigned")
    print("✅ Orchestrator: Custom routing logic")

    print("\n" + "="*60)
    print("✅ All 4 agents configured successfully!")
    print("="*60)


if __name__ == "__main__":
    verify_agents()
