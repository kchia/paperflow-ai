"""
Test individual agents before full integration
"""
from paperflow_agents import (
    inventory_manager,
    quoting_specialist,
    sales_fulfillment,
    financial_controller,
    orchestrator
)
from project_starter import init_database, db_engine

def test_agents():
    """Test each agent with sample requests"""
    
    print("\n" + "🤖"*30)
    print("TESTING PAPERFLOW AI AGENTS")
    print("🤖"*30)
    
    # Initialize database
    print("\nInitializing database...")
    init_database(db_engine, seed=137)
    print("✅ Database ready\n")
    
    test_date = "2025-01-20"
    
    # Test 1: Inventory Manager
    print("="*60)
    print("TEST 1: Inventory Manager")
    print("="*60)
    print("Request: Check stock for A4 paper")
    response = inventory_manager.run(f"Check current stock level for A4 paper (Date: {test_date})")
    print(f"\nResponse:\n{response}\n")
    
    # Test 2: Quoting Specialist
    print("="*60)
    print("TEST 2: Quoting Specialist")
    print("="*60)
    print("Request: Quote for 500 wedding invitations")
    response = quoting_specialist.run(f"Generate a quote for 500 invitation cards for a wedding (Date: {test_date})")
    print(f"\nResponse:\n{response}\n")
    
    # Test 3: Financial Controller
    print("="*60)
    print("TEST 3: Financial Controller")
    print("="*60)
    print("Request: Approve $3000 purchase")
    response = financial_controller.run(f"Check if we can approve a supplier purchase of $3000 (Date: {test_date})")
    print(f"\nResponse:\n{response}\n")
    
    # Test 4: Orchestrator Classification
    print("="*60)
    print("TEST 4: Orchestrator Intent Classification")
    print("="*60)
    test_requests = [
        "Do you have A4 paper in stock?",
        "How much for 1000 business cards?",
        "I'd like to order 500 envelopes",
        "What items do you carry?"
    ]
    
    for req in test_requests:
        intent = orchestrator.classify_intent(req)
        print(f"Request: '{req}'")
        print(f"Classified as: {intent}\n")
    
    # Test 5: Full Orchestrator Workflow
    print("="*60)
    print("TEST 5: Full Orchestrator Workflow")
    print("="*60)
    print("Request: Quote for 200 glossy paper sheets")
    response = orchestrator.route_request(
        "How much would 200 sheets of glossy paper cost?",
        test_date
    )
    print(f"\nFiltered Customer Response:\n{response}\n")
    
    print("="*60)
    print("✅ AGENT TESTS COMPLETED")
    print("="*60)

if __name__ == "__main__":
    test_agents()
