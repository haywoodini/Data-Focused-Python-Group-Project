import os

def main():
    db_script_path = 'DB_building.py'
    if os.path.exists(db_script_path):
        print("Running DB building script...")
        os.system(f'python {db_script_path}')
    else:
        print(f"Error: '{db_script_path}' does not exist.")

    print("Launching Streamlit UI...")
    os.system('streamlit run prototype_ui.py')

if __name__ == "__main__":
    main()
