import subprocess
import sys

def run_commands():
    # Define your list of commands as lists of arguments
    # This prevents command injection vulnerabilities
    commands = [
        ["pyreverse", "-o", "svg", "source/modules", "-S", "-k", "-p", "game", "-d", "docs"],
        ["pyreverse", "-o", "png", "source/modules", "-S", "-k", "-p", "game", "-d", "docs"],
        ["pyreverse", "-o", "puml", "source/modules", "-S", "-k", "-p", "game", "-d", "docs"],
        ["pyreverse", "-o", "mmd", "source/modules", "-S", "-k", "-p", "game", "-d", "docs"],
        ["pyreverse", "-o", "dot", "source/modules", "-S", "-k", "-p", "game", "-d", "docs"]
    ]
    
    for cmd in commands:
        print(f"\n🚀 Running: {' '.join(cmd)}")
        
        try:
            # Execute the command
            result = subprocess.run(
                cmd,
                capture_output=True,  # Saves output instead of printing instantly
                text=True,            # Returns output as a string instead of bytes
                check=True            # Automatically raises an error if the command fails
            )
            
            # Print the success output
            print("✅ Output:")
            print(result.stdout)
            
        except subprocess.CalledProcessError as e:
            # Handle what happens if a single command fails
            print(f"❌ Error executing {' '.join(cmd)}")
            print(f"Exit Code: {e.returncode}")
            print(f"Error Message: {e.stderr}")
            
            # Optional: Stop execution of subsequent commands if one fails
            print("Stopping automation due to error.")
            sys.exit(1)

if __name__ == "__main__":
    run_commands()