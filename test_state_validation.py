#!/usr/bin/env python3
"""
Test the fixed earnings agent
"""
import sys
import os

# Add the backend path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(backend_path)

def test_earnings_state():
    """Test that earnings state initializes properly"""
    from app.agent_core.graphs.earnings_graph import validate_state, AgenticEarningsState
    
    # Test with incomplete state
    incomplete_state = {
        "query": "I earned 100 rupees from Bandra to Andheri",
        "response": ""
    }
    
    print(f"🧪 Testing state validation...")
    print(f"📝 Input state keys: {list(incomplete_state.keys())}")
    
    validated_state = validate_state(incomplete_state)
    print(f"✅ Output state keys: {list(validated_state.keys())}")
    
    required_fields = ["query", "thought", "action", "action_input", "observation", "response", "tools_used", "reasoning_steps"]
    missing_fields = [field for field in required_fields if field not in validated_state]
    
    if missing_fields:
        print(f"❌ Missing fields: {missing_fields}")
    else:
        print(f"✅ All required fields present!")
        print(f"📊 tools_used type: {type(validated_state['tools_used'])}")
        print(f"📊 reasoning_steps type: {type(validated_state['reasoning_steps'])}")

if __name__ == "__main__":
    test_earnings_state()