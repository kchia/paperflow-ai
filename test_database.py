"""
Test script to verify database functions work correctly.
Run this BEFORE implementing agents.
"""
import pandas as pd
from datetime import datetime
from project_starter import (
    init_database,
    db_engine,
    get_stock_level,
    get_all_inventory,
    get_cash_balance,
    generate_financial_report,
    search_quote_history,
    get_supplier_delivery_date,
    create_transaction
)

def test_database_setup():
    """Test 1: Database initialization"""
    print("\n" + "="*60)
    print("TEST 1: Database Initialization")
    print("="*60)
    
    try:
        init_database(db_engine, seed=137)
        print("✅ Database initialized successfully")
        
        # Check tables exist
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", db_engine)
        print(f"✅ Tables created: {tables['name'].tolist()}")
        
    except Exception as e:
        print(f"❌ Database init failed: {e}")
        return False
    
    return True


def test_inventory_functions():
    """Test 2: Inventory functions"""
    print("\n" + "="*60)
    print("TEST 2: Inventory Functions")
    print("="*60)
    
    test_date = "2025-01-15"
    
    try:
        # Test get_all_inventory
        all_inventory = get_all_inventory(test_date)
        print(f"✅ get_all_inventory() returned {len(all_inventory)} items")
        print(f"   Sample items: {list(all_inventory.keys())[:3]}")
        
        # Test get_stock_level for a specific item
        if all_inventory:
            first_item = list(all_inventory.keys())[0]
            stock_df = get_stock_level(first_item, test_date)
            print(f"✅ get_stock_level('{first_item}') = {stock_df['current_stock'].iloc[0]} units")
        
    except Exception as e:
        print(f"❌ Inventory functions failed: {e}")
        return False
    
    return True


def test_financial_functions():
    """Test 3: Financial functions"""
    print("\n" + "="*60)
    print("TEST 3: Financial Functions")
    print("="*60)
    
    test_date = "2025-01-15"
    
    try:
        # Test get_cash_balance
        cash = get_cash_balance(test_date)
        print(f"✅ get_cash_balance() = ${cash:,.2f}")
        
        # Test generate_financial_report
        report = generate_financial_report(test_date)
        print(f"✅ Financial report generated:")
        print(f"   - Cash: ${report['cash_balance']:,.2f}")
        print(f"   - Inventory Value: ${report['inventory_value']:,.2f}")
        print(f"   - Total Assets: ${report['total_assets']:,.2f}")
        print(f"   - Inventory items: {len(report['inventory_summary'])}")
        
    except Exception as e:
        print(f"❌ Financial functions failed: {e}")
        return False
    
    return True


def test_quote_history():
    """Test 4: Quote history search"""
    print("\n" + "="*60)
    print("TEST 4: Quote History Search")
    print("="*60)
    
    try:
        # Test search_quote_history
        results = search_quote_history(["wedding", "invitation"], limit=3)
        print(f"✅ search_quote_history() returned {len(results)} results")
        
        if results:
            print(f"   Sample quote: ${results[0]['total_amount']}")
            print(f"   Job type: {results[0].get('job_type', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Quote history search failed: {e}")
        return False
    
    return True


def test_transaction_creation():
    """Test 5: Transaction creation"""
    print("\n" + "="*60)
    print("TEST 5: Transaction Creation")
    print("="*60)
    
    try:
        # Test create_transaction
        transaction_id = create_transaction(
            item_name="A4 paper",
            transaction_type="sales",
            quantity=50,
            price=2.50,
            date="2025-01-16"
        )
        print(f"✅ create_transaction() successful, ID: {transaction_id}")
        
        # Verify transaction was recorded
        new_cash = get_cash_balance("2025-01-16")
        print(f"✅ Cash balance updated: ${new_cash:,.2f}")
        
    except Exception as e:
        print(f"❌ Transaction creation failed: {e}")
        return False
    
    return True


def test_supplier_delivery():
    """Test 6: Supplier delivery date calculation"""
    print("\n" + "="*60)
    print("TEST 6: Supplier Delivery Date")
    print("="*60)
    
    try:
        # Test different quantities
        test_cases = [
            (10, "small order"),
            (100, "medium order"),
            (500, "large order"),
            (2000, "bulk order")
        ]
        
        for qty, desc in test_cases:
            delivery_date = get_supplier_delivery_date("2025-01-15", qty)
            print(f"✅ {desc} ({qty} units): delivers on {delivery_date}")
        
    except Exception as e:
        print(f"❌ Supplier delivery test failed: {e}")
        return False
    
    return True


def run_all_tests():
    """Run all verification tests"""
    print("\n" + "🔧"*30)
    print("PAPERFLOW AI - DATABASE VERIFICATION SUITE")
    print("🔧"*30)
    
    tests = [
        ("Database Setup", test_database_setup),
        ("Inventory Functions", test_inventory_functions),
        ("Financial Functions", test_financial_functions),
        ("Quote History", test_quote_history),
        ("Transaction Creation", test_transaction_creation),
        ("Supplier Delivery", test_supplier_delivery),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Ready to implement agents.")
        return True
    else:
        print("\n⚠️  Some tests failed. Fix these before proceeding.")
        return False


if __name__ == "__main__":
    run_all_tests()
