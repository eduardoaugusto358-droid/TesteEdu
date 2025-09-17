#!/usr/bin/env python3
"""
Backend Test for WhatsFlow Real - Flows Functionality
Testing the flows API endpoints and visual flow editor functionality
"""

import requests
import json
import uuid
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8889"
API_BASE = f"{BASE_URL}/api"

class FlowsAPITester:
    def __init__(self):
        self.test_results = []
        self.created_flow_ids = []
        
    def log_test(self, test_name, success, message, details=None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details:
            print(f"   Details: {details}")
    
    def test_get_flows(self):
        """Test GET /api/flows endpoint"""
        try:
            response = requests.get(f"{API_BASE}/flows", timeout=10)
            
            if response.status_code == 200:
                flows = response.json()
                self.log_test(
                    "GET /api/flows",
                    True,
                    f"Successfully retrieved {len(flows)} flows",
                    {"status_code": response.status_code, "flow_count": len(flows)}
                )
                return flows
            else:
                self.log_test(
                    "GET /api/flows",
                    False,
                    f"Failed with status {response.status_code}",
                    {"status_code": response.status_code, "response": response.text}
                )
                return None
                
        except Exception as e:
            self.log_test(
                "GET /api/flows",
                False,
                f"Exception occurred: {str(e)}",
                {"error": str(e)}
            )
            return None
    
    def test_create_flow(self):
        """Test POST /api/flows endpoint"""
        try:
            test_flow_data = {
                "name": f"Test Flow {uuid.uuid4().hex[:8]}",
                "description": "Test flow for CRUD operations",
                "nodes": [
                    {
                        "id": "start",
                        "type": "start",
                        "position": {"x": 100, "y": 100},
                        "data": {"label": "Início"}
                    },
                    {
                        "id": "message1",
                        "type": "message",
                        "position": {"x": 300, "y": 100},
                        "data": {"label": "Mensagem de Boas-vindas", "message": "Olá! Como posso ajudar?"}
                    }
                ],
                "edges": [
                    {
                        "id": "e1",
                        "source": "start",
                        "target": "message1"
                    }
                ],
                "active": False,
                "instance_id": None
            }
            
            response = requests.post(
                f"{API_BASE}/flows",
                json=test_flow_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success') and result.get('flow_id'):
                    flow_id = result['flow_id']
                    self.created_flow_ids.append(flow_id)
                    self.log_test(
                        "POST /api/flows",
                        True,
                        f"Successfully created flow with ID: {flow_id}",
                        {"status_code": response.status_code, "flow_id": flow_id}
                    )
                    return flow_id
                else:
                    self.log_test(
                        "POST /api/flows",
                        False,
                        "Response missing success or flow_id",
                        {"status_code": response.status_code, "response": result}
                    )
                    return None
            else:
                self.log_test(
                    "POST /api/flows",
                    False,
                    f"Failed with status {response.status_code}",
                    {"status_code": response.status_code, "response": response.text}
                )
                return None
                
        except Exception as e:
            self.log_test(
                "POST /api/flows",
                False,
                f"Exception occurred: {str(e)}",
                {"error": str(e)}
            )
            return None
    
    def test_update_flow(self, flow_id):
        """Test PUT /api/flows/{id} endpoint"""
        try:
            update_data = {
                "name": f"Updated Test Flow {uuid.uuid4().hex[:8]}",
                "description": "Updated test flow description",
                "active": True,
                "nodes": [
                    {
                        "id": "start",
                        "type": "start",
                        "position": {"x": 100, "y": 100},
                        "data": {"label": "Início Atualizado"}
                    },
                    {
                        "id": "message1",
                        "type": "message",
                        "position": {"x": 300, "y": 100},
                        "data": {"label": "Mensagem Atualizada", "message": "Olá! Mensagem atualizada!"}
                    },
                    {
                        "id": "end",
                        "type": "end",
                        "position": {"x": 500, "y": 100},
                        "data": {"label": "Fim"}
                    }
                ],
                "edges": [
                    {
                        "id": "e1",
                        "source": "start",
                        "target": "message1"
                    },
                    {
                        "id": "e2",
                        "source": "message1",
                        "target": "end"
                    }
                ]
            }
            
            response = requests.put(
                f"{API_BASE}/flows/{flow_id}",
                json=update_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.log_test(
                        "PUT /api/flows/{id}",
                        True,
                        f"Successfully updated flow {flow_id}",
                        {"status_code": response.status_code, "flow_id": flow_id}
                    )
                    return True
                else:
                    self.log_test(
                        "PUT /api/flows/{id}",
                        False,
                        "Response missing success flag",
                        {"status_code": response.status_code, "response": result}
                    )
                    return False
            else:
                self.log_test(
                    "PUT /api/flows/{id}",
                    False,
                    f"Failed with status {response.status_code}",
                    {"status_code": response.status_code, "response": response.text}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "PUT /api/flows/{id}",
                False,
                f"Exception occurred: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    def test_delete_flow(self, flow_id):
        """Test DELETE /api/flows/{id} endpoint"""
        try:
            response = requests.delete(f"{API_BASE}/flows/{flow_id}", timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.log_test(
                        "DELETE /api/flows/{id}",
                        True,
                        f"Successfully deleted flow {flow_id}",
                        {"status_code": response.status_code, "flow_id": flow_id}
                    )
                    return True
                else:
                    self.log_test(
                        "DELETE /api/flows/{id}",
                        False,
                        "Response missing success flag",
                        {"status_code": response.status_code, "response": result}
                    )
                    return False
            else:
                self.log_test(
                    "DELETE /api/flows/{id}",
                    False,
                    f"Failed with status {response.status_code}",
                    {"status_code": response.status_code, "response": response.text}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "DELETE /api/flows/{id}",
                False,
                f"Exception occurred: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    def test_flows_tab_accessibility(self):
        """Test if the Fluxos tab is accessible"""
        try:
            response = requests.get(BASE_URL, timeout=10)
            
            if response.status_code == 200:
                html_content = response.text
                
                # Check if flows section exists in HTML
                flows_indicators = [
                    'id="flows"',
                    'showSection(\'flows\')',
                    'flows-container',
                    'loadFlows()'
                ]
                
                found_indicators = []
                for indicator in flows_indicators:
                    if indicator in html_content:
                        found_indicators.append(indicator)
                
                if len(found_indicators) >= 3:
                    self.log_test(
                        "Fluxos Tab Accessibility",
                        True,
                        f"Fluxos tab found in HTML with {len(found_indicators)}/4 indicators",
                        {"found_indicators": found_indicators}
                    )
                    return True
                else:
                    self.log_test(
                        "Fluxos Tab Accessibility",
                        False,
                        f"Fluxos tab missing or incomplete - only {len(found_indicators)}/4 indicators found",
                        {"found_indicators": found_indicators, "missing": list(set(flows_indicators) - set(found_indicators))}
                    )
                    return False
            else:
                self.log_test(
                    "Fluxos Tab Accessibility",
                    False,
                    f"Failed to load main page - status {response.status_code}",
                    {"status_code": response.status_code}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Fluxos Tab Accessibility",
                False,
                f"Exception occurred: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    def test_visual_flow_editor_components(self):
        """Test if visual flow editor components are present"""
        try:
            response = requests.get(BASE_URL, timeout=10)
            
            if response.status_code == 200:
                html_content = response.text
                
                # Check for visual editor components
                editor_indicators = [
                    'drag-and-drop',
                    'flow-editor',
                    'visual',
                    'renderFlows',
                    'flows-grid',
                    'editFlow',
                    'deleteFlow'
                ]
                
                found_indicators = []
                for indicator in editor_indicators:
                    if indicator in html_content:
                        found_indicators.append(indicator)
                
                if len(found_indicators) >= 4:
                    self.log_test(
                        "Visual Flow Editor Components",
                        True,
                        f"Visual editor components found - {len(found_indicators)}/7 indicators present",
                        {"found_indicators": found_indicators}
                    )
                    return True
                else:
                    self.log_test(
                        "Visual Flow Editor Components",
                        False,
                        f"Visual editor components missing - only {len(found_indicators)}/7 indicators found",
                        {"found_indicators": found_indicators, "missing": list(set(editor_indicators) - set(found_indicators))}
                    )
                    return False
            else:
                self.log_test(
                    "Visual Flow Editor Components",
                    False,
                    f"Failed to load main page - status {response.status_code}",
                    {"status_code": response.status_code}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Visual Flow Editor Components",
                False,
                f"Exception occurred: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    def test_database_flows_table(self):
        """Test if flows are properly saved in SQLite database"""
        try:
            # First create a flow to test database persistence
            flow_id = self.test_create_flow()
            if not flow_id:
                self.log_test(
                    "Database Flows Table",
                    False,
                    "Could not create test flow for database validation",
                    {}
                )
                return False
            
            # Wait a moment for database write
            time.sleep(1)
            
            # Now retrieve flows to verify database persistence
            flows = self.test_get_flows()
            if flows is None:
                self.log_test(
                    "Database Flows Table",
                    False,
                    "Could not retrieve flows from database",
                    {}
                )
                return False
            
            # Check if our created flow exists
            created_flow = None
            for flow in flows:
                if flow.get('id') == flow_id:
                    created_flow = flow
                    break
            
            if created_flow:
                # Verify flow structure
                required_fields = ['id', 'name', 'description', 'nodes', 'edges', 'active', 'created_at', 'updated_at']
                missing_fields = []
                
                for field in required_fields:
                    if field not in created_flow:
                        missing_fields.append(field)
                
                if not missing_fields:
                    self.log_test(
                        "Database Flows Table",
                        True,
                        f"Flow properly saved in database with all required fields",
                        {"flow_id": flow_id, "fields_present": required_fields}
                    )
                    return True
                else:
                    self.log_test(
                        "Database Flows Table",
                        False,
                        f"Flow saved but missing required fields: {missing_fields}",
                        {"flow_id": flow_id, "missing_fields": missing_fields}
                    )
                    return False
            else:
                self.log_test(
                    "Database Flows Table",
                    False,
                    f"Created flow {flow_id} not found in database",
                    {"flow_id": flow_id, "total_flows": len(flows)}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Database Flows Table",
                False,
                f"Exception occurred: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    def test_system_health(self):
        """Test overall system health and connectivity"""
        try:
            # Test main page
            response = requests.get(BASE_URL, timeout=10)
            if response.status_code != 200:
                self.log_test(
                    "System Health",
                    False,
                    f"Main page not accessible - status {response.status_code}",
                    {"status_code": response.status_code}
                )
                return False
            
            # Test API base
            response = requests.get(f"{API_BASE}/flows", timeout=10)
            if response.status_code != 200:
                self.log_test(
                    "System Health",
                    False,
                    f"API not accessible - status {response.status_code}",
                    {"status_code": response.status_code}
                )
                return False
            
            self.log_test(
                "System Health",
                True,
                "System is healthy and accessible",
                {"main_page": "OK", "api": "OK"}
            )
            return True
            
        except Exception as e:
            self.log_test(
                "System Health",
                False,
                f"System health check failed: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    def cleanup_test_flows(self):
        """Clean up test flows created during testing"""
        cleaned_count = 0
        for flow_id in self.created_flow_ids:
            try:
                response = requests.delete(f"{API_BASE}/flows/{flow_id}", timeout=5)
                if response.status_code == 200:
                    cleaned_count += 1
            except:
                pass  # Ignore cleanup errors
        
        if cleaned_count > 0:
            print(f"🧹 Cleaned up {cleaned_count} test flows")
    
    def run_all_tests(self):
        """Run all flow-related tests"""
        print("🚀 Starting WhatsFlow Real - Flows Functionality Tests")
        print("=" * 60)
        
        # Test system health first
        self.test_system_health()
        
        # Test flows API endpoints
        self.test_get_flows()
        
        # Test CRUD operations
        flow_id = self.test_create_flow()
        if flow_id:
            self.test_update_flow(flow_id)
            # Don't delete immediately, let database test use it
        
        # Test database persistence
        self.test_database_flows_table()
        
        # Test UI components
        self.test_flows_tab_accessibility()
        self.test_visual_flow_editor_components()
        
        # Clean up test flows
        self.cleanup_test_flows()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
        
        print("\n✅ PASSED TESTS:")
        for result in self.test_results:
            if result['success']:
                print(f"  - {result['test']}: {result['message']}")
        
        return self.test_results

if __name__ == "__main__":
    tester = FlowsAPITester()
    results = tester.run_all_tests()
    
    # Save results to file
    with open('/app/flows_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📁 Test results saved to: /app/flows_test_results.json")