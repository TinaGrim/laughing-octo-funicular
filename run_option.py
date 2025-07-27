#!/usr/bin/env python3
"""
CLI script to communicate with Option.py class from Java
Usage: python run_option.py <command> [arguments]
"""

import sys
import os
import json

# Add the LD-Player directory to path
LD_Function = os.path.abspath(os.path.join(os.path.dirname(__file__), "LD-Player"))
if LD_Function not in sys.path:
    sys.path.append(LD_Function)

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_option.py <command> [arguments]")
        print("Available commands:")
        print("  open_ld <number>     - Open LD Player instances only")
        print("  open_appium <number> - Open Appium servers only")
        print("  full_start <number>  - Open LD Players + Appium servers")
        print("  setup <number>       - Full setup of LD Players")
        print("  remote <number>      - Start remote drivers")
        print("  get_mail             - Get temporary email")
        print("  random_data          - Get random user data")
        print("  test                 - Test the Option class")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        # Import the Option class
        from Option import option #type: ignore
        opt = option()
        
        if command == "open_ld":
            number = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            print(f"STARTING: Opening {number} LD Player instance(s)...")
            opt.Open_LD(number)
            print("COMPLETED: LD Player instances opened successfully!")
            
        elif command == "full_start":
            number = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            print(f"STARTING: Full setup - Opening {number} LD Player(s) with Appium servers...")
            
            opt.Open_LD(number)
            print(f"Opened {number} LD Player instances")
 
            opt.Full_setup(number)
            print("COMPLETED: LD Player setup completed!")
            
            opt.Remote_Driver(number)
            print("COMPLETED: Remote drivers started!")
        elif command == "setup":
            number = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            print(f"STARTING: Setting up {number} LD Player instance(s)...")
            opt.Full_setup(number)
            print("COMPLETED: LD Player setup completed!")
            
        elif command == "remote":
            number = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            print(f"STARTING: Starting {number} remote driver(s)...")
            opt.Remote_Driver(number)
            print("COMPLETED: Remote drivers started!")
            
        else:
            print(f"ERROR: Unknown command: {command}")
            sys.exit(1)
            
    except ImportError as e:
        print(f"ERROR: Error importing Option class: {e}")
        print("Make sure Option.py is in the LD-Player directory")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Error executing command '{command}': {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
