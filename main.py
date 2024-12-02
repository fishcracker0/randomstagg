import os
import shutil
from app import ApplicationManager, RobloxManager

def delete_cli_directory():
    cli_path = "/data/data/com.termux/files/home/.cli"
    if os.path.exists(cli_path):
        try:
            shutil.rmtree(cli_path)
            print(f"Deleted directory: {cli_path}")
        except Exception as e:
            print(f"Failed to delete directory {cli_path}: {e}")
    else:
        print(f"Directory {cli_path} does not exist.")

def main():
    delete_cli_directory()
    
    app_manager = ApplicationManager()
    roblox_manager = RobloxManager()
    
    app_manager.run()
    
    while True:
        roblox_manager.display_panel_with_header()
        
        user_choice = roblox_manager.prompt_user_choice()
        
        if user_choice == '1':
            if not roblox_manager.start_auto_rejoin():
                roblox_manager.console.print("[red]Failed to load config from JSON. Please select option 2 to set up the autorejoin config.[/red]")
                roblox_manager.press_enter_to_continue()
        elif user_choice == '2':
            if roblox_manager.manage_packages():
                roblox_manager.console.print("[green]Configuration successful; you can start auto-rejoin now![/green]")
            else:
                roblox_manager.console.print("[red]Failed to configure auto setup[/red]")    
            roblox_manager.press_enter_to_continue()
        elif user_choice == '3':
            user_choice_bypass = roblox_manager.prompt_user_choice_bypass()
            if user_choice_bypass == '1':   
                if not roblox_manager.start_auto_rejoin():
                    roblox_manager.console.print("[red]Failed to load config from JSON. Please select option 2 to set up the autorejoin config.[/red]")
                    roblox_manager.press_enter_to_continue()
            elif user_choice_bypass == '2' or user_choice_bypass == '3':
                if not roblox_manager.codex_arcuesx_bypass():
                    roblox_manager.console.print("[red]Failed to bypass.[/red]")
                    roblox_manager.press_enter_to_continue()
            elif user_choice_bypass == '4':
                roblox_manager.press_enter_to_continue()
        elif user_choice == '4':
            roblox_manager.display_configuration()
            roblox_manager.press_enter_to_continue()
        elif user_choice == '5':
            roblox_manager.inject_cookies_and_appstorage()
            roblox_manager.press_enter_to_continue()
        elif user_choice == '8':
            if roblox_manager.clear_json_file(roblox_manager.json_file_path) and roblox_manager.clear_json_file(roblox_manager.hwid_path):
                roblox_manager.console.print(f"Data cleared, please setup again to continue using the rejoin tool")
            else:
                roblox_manager.console.print(f"Failed to clear data")
                roblox_manager.press_enter_to_continue()
        elif user_choice == '9':
            break
        else:
            roblox_manager.console.print(f"[red]Invalid choice please choose from 1-9[/red]")
            roblox_manager.press_enter_to_continue()

if __name__ == "__main__":
    main()