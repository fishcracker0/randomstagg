_O="[red]Invalid input. Please enter a valid game ID (long integer) or a link starting with 'https://www.roblox.com/share?code='. Please try again.[/red]"
_N='https://www.roblox.com/share?code='
_M='green'
_L='yellow'
_K='Package'
_J='server_link'
_I='cyan'
_H='left'
_G='Username'
_F='UserId'
_E='['
_D=False
_C='Status'
_B='magenta'
_A=True
import os,json,time,subprocess,psutil,requests,subprocess,sqlite3,shutil,re
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.color import Color
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner
from rich.progress import Progress,SpinnerColumn,BarColumn,TextColumn
from typing import List
class RobloxManager:
	CHECK_INTERVAL=180;RESTART_INTERVAL=3600;FLUXUS_BYPASS_INTERVAL=60;FIXED_ANDROID_ID='b419fa14320149db'
	def __init__(A):super().__init__();A.console=Console();A.installed_roblox_packages=[];A.base_package='com.roblox';A.user_choice='';A.user_choice_bypass='';A.LOGO=A.create_logo();A.user_data={};A.server_link_delay=20;A.status={};A.username={};A.user_ids={};A.server_links={};A.last_locations={};A.last_restart_time=time.time();A.json_file_path='/storage/emulated/0/Download/user_data.json';A.hwid_path='/storage/emulated/0/Download/hwid.json';A.hwid_directory_path='/data/data/com.roblox.client/app_assets/content/';A.session=requests.Session()
	def check_permission(B):'Check if the script has root permissions.';A=subprocess.run(['id','-u'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);return A.returncode==0
	def clear_screen(A):
		if os.name=='posix':os.system('clear')
		else:A.console.print('\x1b[2J\x1b[H')
	def create_logo(B):A='\n███████╗  ███████╗  ██████╗  ██████╗  ███╗   ██╗ ███╗   ██╗ ███████╗  ██████╗ ████████╗\n██ ╔══██╗ ██╔════╝ ██╔════╝ ██╔═══██╗ ████╗  ██║ ████╗  ██║ ██╔════╝ ██╔════╝ ╚══██╔══╝\n███████╔╝ █████╗   ██║      ██║   ██║ ██╔██╗ ██║ ██╔██╗ ██║ █████╗   ██║         ██║\n██╔══██╗  ██╔══╝   ██║      ██║   ██║ ██║╚██╗██║ ██║╚██╗██║ ██╔══╝   ██║         ██║\n██║  ██║  ███████╗ ╚██████╗ ╚██████╔╝ ██║ ╚████║ ██║ ╚████║ ███████╗ ╚██████╗    ██║\n╚═╝  ╚═╝  ╚══════╝  ╚═════╝  ╚═════╝  ╚═╝  ╚═══╝ ╚═╝  ╚═══╝ ╚══════╝  ╚═════╝    ╚═╝\n        ';return A
	def create_menu(B):A=Text();A.append('\n[').append('1',style=_B).append('] Start Auto Rejoin\n');A.append(_E).append('2',style=_B).append('] Start Auto Setup\n');A.append(_E).append('3',style=_B).append('] Start Auto Bypass\n');A.append(_E).append('4',style=_B).append('] Show List\n');A.append(_E).append('5',style=_B).append('] Auto Login via Cookie\n');A.append(_E).append('6',style=_B).append('] Auto Change Account via Cookie (Blox Fruit Only)\n');A.append(_E).append('7',style=_B).append('] Add auto execute script\n');A.append(_E).append('8',style=_B).append('] Clear Configuration\n');A.append(_E).append('9',style=_B).append('] Exit\n');return A
	def create_menu_bypass(B):A=Text();A.append(_E).append('1',style=_B).append('] Fluxus\n');A.append(_E).append('2',style=_B).append('] Codex\n');A.append(_E).append('3',style=_B).append('] ArceusX\n');A.append(_E).append('4',style=_B).append('] Exit');return A
	def interpolate_color(K,color1,color2,factor):A=factor;B,C,D=color1.get_truecolor();E,F,G=color2.get_truecolor();H=int(B+A*(E-B));I=int(C+A*(F-C));J=int(D+A*(G-D));return f"#{H:02x}{I:02x}{J:02x}"
	def create_smooth_gradient_logo(B):
		E=Color.parse(_B);F=Color.parse(_I);C=B.LOGO.strip().split('\n');G=sum(len(A)for A in C);A=Text();D=0
		for H in C:
			for I in H:J=D/G;K=B.interpolate_color(E,F,J);A.append(I,style=f"bold {K}");D+=1
			A.append('\n')
		return A
	def print_header(A):B=A.create_smooth_gradient_logo();A.console.print(B)
	def get_package_path(A,package_name):'Generate the path for the given package name.';return f"/data/data/{package_name}/files/appData/LocalStorage/appStorage.json"
	def load_json_from_path(C,file_path):
		'Load the Username and UserId from the given path.';E='Unknown';B=file_path;A=None
		try:
			with open(B,'r')as F:D=json.load(F);G=D.get(_G,E);H=D.get(_F,E);return G,H
		except FileNotFoundError:C.console.print(f"[red]File not found:[/red] {B}");return A,A
		except json.JSONDecodeError:C.console.print(f"[red]Error decoding JSON:[/red] {B}");return A,A
		except PermissionError:C.console.print(f"[red]Permission denied:[/red] {B}");return A,A
	def check_installed_roblox_variants(A):
		"Check for installed Roblox package variants of 'com.roblox.client'.";A.installed_roblox_packages.clear();B=subprocess.run(['pm','list','packages'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=_A)
		if B.returncode!=0:print(f"Error executing command: {B.stderr}");return[]
		C=B.stdout.splitlines();D=[A.replace('package:','')for A in C];E=re.compile(f"^{A.base_package}.");A.installed_roblox_packages=[A for A in D if E.match(A)];return A.installed_roblox_packages
	def print_installed_packages(A):
		if not A.installed_roblox_packages:A.logger.info('No Roblox package variants found')
		else:
			A.logger.info('Installed Roblox package variants:')
			for B in A.installed_roblox_packages:A.logger.info(f"- {B}")
	def display_panel_with_header(A):
		A.print_header();B=A.console.size.width;F=A.console.size.height
		if B>120:C=int(B*.5)
		else:C=int(B*.85)
		D=A.create_menu();E=Panel(D,title='Tool Menu',width=C,border_style=_I);A.console.print(E)
	def save_user_data_to_json(A,file_path):
		'Save the user data to a JSON file.'
		try:
			with open(file_path,'w')as B:json.dump(A.user_data,B,indent=4)
		except Exception as C:A.console.print(f"[red]Failed to save user data:[/red] {C}")
	def prompt_for_server_link(B):
		'Prompt the user for the server link for individual packages with validation.'
		while _A:
			A=B.console.input('[yellow]Please enter the server link or game ID for this package:[/yellow] ')
			if A.isdigit():C=f"roblox://placeid={A}";return C
			elif A.startswith(_N):return A
			else:B.console.print(_O)
	def prompt_for_common_server_link(B):
		'Prompt the user for a common server link for all packages with validation.'
		while _A:
			A=B.console.input('[yellow]Please enter a common server link or game ID for all packages:[/yellow] ')
			if A.isdigit():C=f"roblox://placeid={A}";return C
			elif A.startswith(_N):return A
			else:B.console.print(_O)
	def prompt_user_choice(A):B=A.console.input('\n[yellow bold]Please enter a number from the menu above:[/yellow bold] ');A.user_choice=B;return B
	def prompt_user_choice_bypass(A):A.console.print(A.create_menu_bypass());B=A.console.input('\n[yellow bold]Please choose executor to bypass (1-4):[/yellow bold] ');A.user_choice_bypass=B;return B
	def manage_packages(A):
		'Main function to check permissions, load packages, and store Username/UserId.'
		if not A.check_permission():A.console.print('[red]Permission denied: You need to run this script with root privileges.[/red]');return _D
		A.check_installed_roblox_variants();F=A.console.input('[yellow]Do you want to use the same server link for all packages? (Y/N): [/yellow]').strip().upper()
		if F=='Y':K=A.prompt_for_common_server_link()
		B=Progress('{task.description}',SpinnerColumn(),BarColumn(),TextColumn('[progress.percentage]{task.percentage:>3.0f}%'));L=len(A.installed_roblox_packages);G=Progress();M=G.add_task('Overall Progress',total=L)
		with Live(B,refresh_per_second=10)as C:
			for E in A.installed_roblox_packages:
				D=B.add_task(f"Processing {E}",total=100);time.sleep(.5);B.update(D,advance=30);C.refresh();N=A.get_package_path(E);H,I=A.load_json_from_path(N)
				if H and I:
					if F=='Y':J=K
					else:C.stop();J=A.prompt_for_server_link();C.start()
					A.user_data[E]={_G:H,_F:I,_J:J};time.sleep(.5);B.update(D,advance=50);C.refresh()
				else:B.update(D,advance=50)
				B.update(D,advance=20);G.update(M,advance=1);C.refresh()
		A.save_user_data_to_json(A.json_file_path);return _A
	def display_user_data(B,file_path):
		'Display user data in a table format.';C=file_path
		try:
			with open(C,'r')as E:F=json.load(E)
			A=Table(title='User Data');A.add_column(_G,justify=_H,style=_I);A.add_column(_F,justify=_H,style=_B);A.add_column(_K,justify=_H,style=_L);A.add_column('ServerLink',justify=_H,style=_M)
			for(G,D)in F.items():A.add_row(D[_G],D[_F],G,D[_J])
			B.console.print(A)
		except FileNotFoundError:B.console.print(f"[red]File not found:[/red] {C}")
		except json.JSONDecodeError:B.console.print(f"[red]Error decoding JSON:[/red] {C}")
		except Exception as H:B.console.print(f"[red]An error occurred:[/red] {H}")
	def open_roblox(C,package_name):'Open the Roblox app with the given package name.';A=f"am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -n {package_name}/com.roblox.client.startup.ActivitySplash";B=subprocess.run(A,shell=_A,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);return B.returncode==0
	def kill_roblox_process(C,package_name):
		'Force stop the specified Roblox package using Termux commands.'
		try:A=f"am force-stop {package_name}";B=subprocess.run(A,shell=_A,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,text=_A);return B.returncode==0
		except Exception:return _D
	def open_server_link(B,package_name,server_link):
		'Open the server link in the Roblox app with the given package name.';A=server_link;time.sleep(B.server_link_delay)
		if not A:return _D
		C=f'am start -n {package_name}/com.roblox.client.ActivityProtocolLaunch -a android.intent.action.VIEW -d "{A}"';D=subprocess.run(C,shell=_A,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);return D.returncode==0
	def is_roblox_running(C,package_name):
		A='name'
		for B in psutil.process_iter([A]):
			if package_name in B.info[A].lower():return _A
		return _D
	def launch_roblox(A,package_name,server_link):
		'Complete task for killing, opening and joining roblox';B=package_name;A.initialize_data_for_table()
		if not A.is_roblox_running(B):
			if A.kill_roblox_process(B):A.status[B][_C]=f"[blue]Killing roblox....[/blue]"
			A.display_status_table()
		A.status[B][_C]=f"[blue]Opening roblox....[/blue]";A.display_status_table()
		if A.open_roblox(B):A.status[B][_C]=f"Successfully open roblox"
		else:A.status[B][_C]=f"[red]Failed to open roblox....[/red]"
		A.display_status_table()
		if A.open_server_link(B,server_link):A.status[B][_C]=f"[blue]Joining roblox....[/blue]"
		else:A.status[B][_C]=f"[red]Failed to  roblox....[/red]"
		A.display_status_table();A.status[B][_C]=f"Successfully joined roblox";A.display_status_table()
	def display_status_table(B):
		'Display the status table of all package operations with a spinner for ongoing tasks.'
		def A():
			'Generate the table with package status and spinner where necessary.';H='....';A=Table(title='Package Operation Status');A.add_column(_G,justify=_H,style=_I);A.add_column(_F,justify=_H,style=_B);A.add_column(_K,justify=_H,style=_L);A.add_column(_C,justify=_H,style=_M)
			for(C,E)in B.user_data.items():
				F=E[_G];G=E[_F];D=B.status.get(C,{}).get(_C,'Waiting......')
				if H in D:I=Spinner('dots8',text=D.strip(H));A.add_row(F,G,C,I)
				else:A.add_row(F,G,C,D)
			return A
		B.clear_screen();B.print_header()
		with Live(A(),refresh_per_second=20,console=B.console):time.sleep(1)
	def display_configuration(B):
		'Display the status table of all package operations with a spinner for ongoing tasks.'
		if not B.load_config_from_json():return _D
		B.clear_screen();B.print_header();A=Table(title='User Information');A.add_column(_G,style=_B);A.add_column(_F,style=_M);A.add_column('Server Link',style=_L);A.add_column(_K,style=_I,no_wrap=_A)
		for(D,C)in B.user_data.items():A.add_row(C[_G],C[_F],C[_J],D)
		B.console.print(A)
	def load_config_from_json(A):
		'Load user data from JSON file and set up configuration.'
		try:
			with open(A.json_file_path,'r')as D:
				A.user_data=json.load(D)
				for(B,C)in A.user_data.items():
					if _F in C and _J in C:A.installed_roblox_packages.append(B);A.user_ids[B]=int(C[_F]);A.server_links[B]=C[_J]
					else:A.console.print(f"[yellow]Missing 'UserId' or 'server_link' for {B} in JSON data.[/yellow]");return _D
				return _A
		except FileNotFoundError:A.console.print(f"[red]Config file not found at {A.json_file_path}. Please check the path.[/red]")
		except json.JSONDecodeError:A.console.print('[red]Error parsing JSON file. Check the file format.[/red]')
		return _D
	def fetch_presence(C,user_ids_list):
		'Fetch presence data for the given list of user IDs.\n        Returns a dict mapping user_id to presence data.\n        ';D=user_ids_list;A={}
		if not D:return A
		F='https://presence.roproxy.com/v1/presence/users';G={'Content-Type':'application/json'};H={'userIds':D}
		try:
			B=requests.post(F,headers=G,json=H,timeout=10)
			if B.status_code==200:
				I=B.json();J=I.get('userPresences',[])
				for E in J:K=E.get('userId');A[K]=E
			else:C.console.print(f"Failed to fetch presence. Status code: {B.status_code}")
		except requests.RequestException as L:C.console.print(f"Error fetching presence data: {L}")
		return A
	def get_package_name_by_user_id(C,user_id,user_data):
		for(A,B)in user_data.items():
			if B==user_id:return A
	def press_enter_to_continue(A):A.console.input('Press Enter to continue...');A.clear_screen()
	def fetch_fluxus_data(B,fluxus_hwid):
		'Fetch data from the Fluxus API using the provided HWID.';C=f"https://prince-mysticmoth-api.vercel.app/api/fluxus?link=https://flux.li/android/external/start.php?HWID={fluxus_hwid}&apikey=Triple_0H9BP72"
		try:
			A=requests.get(C)
			if A.status_code==200:D=A.json();return D
			else:B.console.print(f"Failed to fetch data. Status code: {A.status_code}")
		except requests.RequestException as E:B.console.print(f"Error fetching data: {E}")
	def get_fluxus_hwid_from_file(A):
		'Get the Fluxus HWID from the file with a 96-character filename.'
		try:
			B=subprocess.run(['ls',A.hwid_directory_path],capture_output=_A,text=_A)
			if B.returncode==0:
				E=B.stdout.splitlines()
				for C in E:
					if len(C)==96:
						F=f"{A.hwid_directory_path}{C}";D=subprocess.run(['cat',F],capture_output=_A,text=_A)
						if D.returncode==0:return D.stdout.strip()
						else:A.console.print(f"Failed to read {C}: {D.stderr}")
			else:A.console.print(f"Error accessing directory: {B.stderr}")
		except Exception as G:A.console.print(f"An error occurred: {G}")
	def save_hwid(A,package_name,hwid):
		'Save the HWID to a JSON file.'
		try:
			with open(A.hwid_path,'w')as B:json.dump({package_name:hwid},B)
			print(f"HWID saved to {A.hwid_path}")
		except Exception as C:print(f"Error saving HWID: {C}")
	def check_hwid_file_exists(A):'Check if the HWID JSON file exists.';return os.path.exists(A.hwid_path)
	def initialize_data_for_table(A):
		for B in A.installed_roblox_packages:
			if B not in A.status:A.status[B]={}
	def perform_fluxus_bypass(A):
		for B in A.installed_roblox_packages:
			A.status[B][_C]=f"[blue]Performing Fluxus bypass....[/blue]";A.display_status_table();C=A.get_fluxus_hwid_from_file()
			if C:
				if not A.check_hwid_file_exists():A.save_hwid(B,C)
				D=A.fetch_fluxus_data(C)
				if D['message']=='Fluxus bypass successful':A.status[B][_C]=f"Fluxus bypass successful"
				else:A.status[B][_C]=f"[red]Failed to bypass fluxus[/red]"
			A.display_status_table()
	def start_auto_rejoin(A):
		'Start running the tool with an initial Fluxus bypass and periodic re-bypass based on interval.'
		if not A.load_config_from_json():return _D
		A.initialize_data_for_table()
		if A.user_choice=='3'and A.user_choice_bypass=='1':A.perform_fluxus_bypass();F=time.time()
		G=time.time()
		while _A:
			if A.user_choice=='3'and A.user_choice_bypass=='1':
				if time.time()-F>=A.FLUXUS_BYPASS_INTERVAL:A.perform_fluxus_bypass();F=time.time()
			C=list(A.user_ids.values())
			if not C:A.console.print('No user IDs assigned, please setup configuration first.');return _D
			J=time.time()
			while time.time()-J<A.CHECK_INTERVAL:
				K=A.fetch_presence(C)
				for D in C:
					B=A.get_package_name_by_user_id(D,A.user_ids);A.status[B][_C]=f"[blue]Starting rejoin....[/blue]";A.display_status_table()
					if not B:A.status[B][_C]=f"[red]Error no package found[/red]";continue
					E=K.get(D)
					if not E:A.status[B][_C]=f"[red]Error no data found[/red]";continue
					H=E.get('lastLocation','').strip();I=E.get('userPresenceType',0)
					if I in[0,1]or H=='Website':A.launch_roblox(B,A.server_links.get(B))
					elif I==2:A.status[B][_C]=f"Account is in-game"
					else:A.status[B][_C]=f"Error processing..."
					A.last_locations[D]=H
				time.sleep(180)
			if time.time()-G>=A.RESTART_INTERVAL:
				A.console.print('Performing scheduled restarts for all packages.')
				for B in A.installed_roblox_packages:A.launch_roblox(B,A.server_links.get(B))
				G=time.time()
	def clear_json_file(B,file_path):
		'Clear all data from a JSON file by overwriting it with an empty dictionary.'
		try:
			with open(file_path,'w')as A:json.dump({},A)
			return _A
		except Exception as C:return _D
	def codex_arcuesx_bypass(A):
		'Change the Android ID.'
		try:os.system(f"settings put secure android_id {A.FIXED_ANDROID_ID}");A.console.print(f"[green]Bypass successfully....[/green]");A.start_auto_rejoin();return _A
		except Exception as B:A.console.print(f"[red]Error: Failed to bypass.[/red]");return _D
	def verify_cookie(A,cookie_value):
		C='https://www.roblox.com/';D={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36','Accept-Language':'en-US,en;q=0.9','Accept':'*/*','Connection':'keep-alive','Referer':C,'Origin':'https://www.roblox.com','Cookie':f".ROBLOSECURITY={cookie_value}"};time.sleep(1);B=A.session.get(C,headers=D);print(B)
		if B.status_code==200:
			try:A.console.print(f"[green]Cookie is valid![/green]");return _A
			except UnicodeEncodeError:A.console.print(f"[green]Cookie is valid![/green]");return _A
		if B.status_code==403:
			try:A.console.print(f"[red]Cookie is invalid![/red]");return _D
			except UnicodeEncodeError:A.console.print(f"[red]Cookie is invalid![/red]");return _D
		try:A.console.print(f"[red]Error verifying cookie: {B.status_code} - {B.text}[/red]")
		except UnicodeEncodeError:A.console.print(f"[red]Error verifying cookie: {B.status_code} - {B.text}[/red]")
		return _D
	def download_file(B,url,destination,binary=_A):
		D=binary;A=destination;C=requests.get(url,stream=_A)
		if C.status_code==200:
			F='wb'if D else'w'
			with open(A,F)as E:
				if D:shutil.copyfileobj(C.raw,E)
				else:E.write(C.text)
			try:B.console.print(f"[green]{os.path.basename(A)} downloaded successfully.[/green]")
			except UnicodeEncodeError:B.console.print(f"[green]{os.path.basename(A)} downloaded successfully.[/green]")
			return A
		try:B.console.print(f"[red]Failed to download {os.path.basename(A)}[/red]")
		except UnicodeEncodeError:B.console.print(f"[red]Failed to download {os.path.basename(A)}.[/red]")
	def replace_cookie_value_in_db(C,db_path,new_cookie_value):
		E='[green]Cookie value successfully replaced in database.[/green]';D=new_cookie_value;B=sqlite3.connect(db_path);A=B.cursor();A.execute('SELECT COUNT(*) FROM cookies');F=A.fetchone()[0]
		if F:A.execute("UPDATE cookies SET value = ?, expires_utc = ?, is_secure = ? WHERE name = '.ROBLOXSECURITY'",(D,int(time.time()*1000),1))
		A.execute('INSERT OR REPLACE INTO cookies (expires_utc, value, creation_utc) VALUES (?, ?, ?)',(int(time.time()*1000),D,int(time.time()*1000)));B.commit();B.close()
		try:C.console.print(E)
		except UnicodeEncodeError:C.console.print(E)
	def get_cookie_path(A,package_name):'Generate the path for the given package name.';return f"/data/data/{package_name}/app_webview/Default/"
	def get_appstorage_path(A,package_name):'Generate the path for the given package name.';return f"/data/data/{package_name}/files/appData/LocalStorage/"
	def inject_cookies_and_appstorage(A):
		K='[red]Failed to download Cookies.db or appStorage.json. Skipping injection.[/red]';J='appStorage.json';A.check_installed_roblox_variants();L='https://raw.githubusercontent.com/fishcracker0/sample/refs/heads/main/Cookies';M='https://raw.githubusercontent.com/fishcracker0/sample/refs/heads/main/appStorage.json';E=A.download_file(L,'Cookies.db',binary=_A);F=A.download_file(M,J,binary=_A)
		if not E or not F:
			try:A.console.print(K)
			except UnicodeEncodeError:A.console.print(K)
			return
		for B in A.installed_roblox_packages:
			while _A:
				C=A.console.input(f"[yellow bold]Please enter a cookie for {B}")
				if A.verify_cookie(C):
					A.console.print(f"[green]Cookie for {B} is valid![/green]");G=A.get_cookie_path(B);H=A.get_appstorage_path(B);os.makedirs(G,exist_ok=_A);os.makedirs(H,exist_ok=_A);D=os.path.join(G,'Cookies');shutil.copyfile(E,D);A.console.print(f"[green]Copied Cookies.db to {D}[/green]");I=os.path.join(H,J);shutil.copyfile(F,I);A.console.print(f"[green]Copied appStorage.json to {I}[/green]");A.replace_cookie_value_in_db(D,C)
					if A.verify_cookie(C):A.console.print(f"[green]Cookie for {B} is valid after injection![/green]")
					else:A.console.print(f"[red]Cookie for {B} is invalid after injection![/red]")
					A.console.print(f"[green]Cookies and appStorage injected successfully.[/green]");break
				else:A.console.print(f"[red]Cookie for {B} is invalid!. Please try again.[/red]")