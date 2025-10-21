"""
Test script for PaperFlow AI tools
"""
from paperflow_tools import *
from project_starter import init_database, db_engine

def test_all_tools():
    """Test each tool individually"""
    
    print("\n" + "🔧"*30)
    print("TESTING PAPERFLOW AI TOOLS")
    print("🔧"*30)
    
    # Initialize database
    print("\nInitializing database...")
    init_database(db_engine, seed=137)
    print("✅ Database ready")
    
    test_date = "2025-01-15"
    
    # Test Inventory Manager Tools
    print("\n" + "="*60)
    print("INVENTORY MANAGER TOOLS")
    print("="*60)
    
    print("\n1. check_stock_level:")
    print(check_stock_level("A4 paper", test_date))
    
    print("\n2. list_all_available_items:")
    print(list_all_available_items(test_date)[:300] + "...")
    
    print("\n3. check_if_reorder_needed:")
    print(check_if_reorder_needed("A4 paper", test_date))
    
    print("\n4. place_supplier_order:")
    print(place_supplier_order("A4 paper", 100, test_date))
    
    # Test Quoting Specialist Tools
    print("\n" + "="*60)
    print("QUOTING SPECIALIST TOOLS")
    print("="*60)
    
    print("\n5. search_similar_quotes:")
    print(search_similar_quotes("paper,office", 3))
    
    print("\n6. calculate_price_with_discounts:")
    print(calculate_price_with_discounts("A4 paper", 500, test_date))
    
    print("\n7. generate_customer_quote:")
    print(generate_customer_quote("A4 paper", 500, test_date, 
                                  "Office supply order"))
    
    # Test Sales Fulfillment Tools
    print("\n" + "="*60)
    print("SALES FULFILLMENT TOOLS")
    print("="*60)
    
    print("\n8. validate_order_feasibility:")
    print(validate_order_feasibility("A4 paper", 100, test_date))
    
    print("\n9. complete_sale_transaction:")
    print(complete_sale_transaction("A4 paper", 50, 125.50, test_date))
    
    # Test Financial Controller Tools
    print("\n" + "="*60)
    print("FINANCIAL CONTROLLER TOOLS")
    print("="*60)
    
    print("\n10. get_current_cash_balance:")
    print(get_current_cash_balance(test_date))
    
    print("\n11. approve_supplier_purchase:")
    print(approve_supplier_purchase(5000.0, test_date))
    
    print("\n" + "="*60)
    print("✅ ALL TOOLS TESTED SUCCESSFULLY")
    print("="*60)

if __name__ == "__main__":
    test_all_tools()
