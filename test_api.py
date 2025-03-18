import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"  # Change this if your API is running on a different URL

def test_api():
    print("Testing FastAPI REST API...")
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print(f"✅ Health check successful: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error connecting to API: {str(e)}")
        print("Make sure the API is running and the URL is correct.")
        return False
    
    # Test root endpoint
    print("\n2. Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"✅ Response: {response.json()}")
    
    # Test creating an item
    print("\n3. Testing item creation...")
    item_data = {
        "name": "Test Item",
        "price": 29.99,
        "description": "This is a test item created by the test script"
    }
    response = requests.post(f"{BASE_URL}/items", json=item_data)
    
    if response.status_code == 201:
        print(f"✅ Item created successfully: {response.json()}")
        item_id = response.json()["id"]
    else:
        print(f"❌ Failed to create item: {response.status_code}, {response.text}")
        return False
    
    # Test getting all items
    print("\n4. Testing get all items...")
    response = requests.get(f"{BASE_URL}/items")
    if response.status_code == 200:
        items = response.json()
        print(f"✅ Retrieved {len(items)} items")
    else:
        print(f"❌ Failed to get items: {response.status_code}")
    
    # Test getting specific item
    print(f"\n5. Testing get item by ID ({item_id})...")
    response = requests.get(f"{BASE_URL}/items/{item_id}")
    if response.status_code == 200:
        print(f"✅ Item retrieved: {response.json()}")
    else:
        print(f"❌ Failed to get item: {response.status_code}")
    
    # Test updating an item
    print(f"\n6. Testing update item ({item_id})...")
    updated_data = {
        "name": "Updated Test Item",
        "price": 39.99,
        "description": "This item has been updated"
    }
    response = requests.put(f"{BASE_URL}/items/{item_id}", json=updated_data)
    if response.status_code == 200:
        print(f"✅ Item updated: {response.json()}")
    else:
        print(f"❌ Failed to update item: {response.status_code}")
    
    # Test deleting an item
    print(f"\n7. Testing delete item ({item_id})...")
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    if response.status_code == 204:
        print("✅ Item deleted successfully")
    else:
        print(f"❌ Failed to delete item: {response.status_code}")
    
    # Verify deletion
    print("\n8. Verifying deletion...")
    response = requests.get(f"{BASE_URL}/items/{item_id}")
    if response.status_code == 404:
        print("✅ Verification successful - item no longer exists")
    else:
        print(f"❌ Verification failed: {response.status_code}")
    
    print("\n✅ All tests completed successfully!")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
        print(f"Using custom base URL: {BASE_URL}")
    
    test_api() 