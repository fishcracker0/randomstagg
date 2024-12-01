import os,time,subprocess
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich.live import Live
from rich.spinner import Spinner
from rich.color import Color
class ApplicationManager:
	REQUIRED_MODULES=['os','json','time','subprocess','psutil','requests','rich.console','rich.panel','rich.text','rich.layout','rich.align','rich.live','rich.spinner','rich.color'];LOGO='\n██████╗  ███████╗  ██████╗   ██████╗ ███╗   ██╗ ███╗   ██╗ ███████╗  ██████╗ ████████╗\n██╔══██╗ ██╔════╝ ██╔════╝ ██╔═══██╗ ████╗  ██║ ████╗  ██║ ██╔════╝ ██╔════╝ ╚══██╔══╝\n██████╔╝ █████╗   ██║      ██║   ██║ ██╔██╗ ██║ ██╔██╗ ██║ █████╗   ██║         ██║   \n██╔══██╗ ██╔══╝   ██║      ██║   ██║ ██║╚██╗██║ ██║╚██╗██║ ██╔══╝   ██║         ██║   \n██║  ██║ ███████╗ ╚██████╗ ╚██████╔╝ ██║ ╚████║ ██║ ╚████║ ███████╗ ╚██████╗    ██║   \n╚═╝  ╚═╝ ╚══════╝  ╚═════╝  ╚═════╝  ╚═╝  ╚═══╝ ╚═╝  ╚═══╝ ╚══════╝  ╚═════╝    ╚═╝   \n    '
	def __init__(A):A.console=Console()
	def check_modules(C):
		'Check if required modules are installed';A=[]
		for B in C.REQUIRED_MODULES:
			try:__import__(B.split('.')[0])
			except ImportError:A.append(B)
		return A
	def install_modules(A,missing_modules):
		'Install missing modules using pip';A.console.print('[yellow]Missing modules detected, attempting to install...[/yellow]')
		for B in missing_modules:
			try:subprocess.check_call([os.sys.executable,'-m','pip','install',B]);A.console.print(f"[green]Successfully installed {B}[/green]")
			except subprocess.CalledProcessError:A.console.print(f"[red]Failed to install {B}. Please install it manually.[/red]")
	def interpolate_color(K,color1,color2,factor):A=factor;B,C,D=color1.get_truecolor();E,F,G=color2.get_truecolor();H=int(B+A*(E-B));I=int(C+A*(F-C));J=int(D+A*(G-D));return f"#{H:02x}{I:02x}{J:02x}"
	def create_smooth_gradient_logo(B):
		'Create a smooth color gradient for the logo';E=Color.parse('magenta');F=Color.parse('cyan');C=B.LOGO.strip().split('\n');G=sum(len(A)for A in C);A=Text();D=0
		for H in C:
			for I in H:J=D/G;K=B.interpolate_color(E,F,J);A.append(I,style=f"bold {K}");D+=1
			A.append('\n')
		return A
	def splash_screen(B):
		'Display the splash screen with the gradient logo and loading spinner';E='lower';D='upper';A=Layout();A.split_column(Layout(name=D,ratio=2),Layout(name=E,ratio=1));F=B.create_smooth_gradient_logo();G=Panel(Align.center(F,vertical='middle'));A[D].update(G);H=Spinner('aesthetic',style='green');C=0;I=time.time()
		def J():A=time.time()-I;B=H.render(A);D=Text(f" Loading... {C}%",style='bold green');E=Text.assemble(B,D);return Align.center(E)
		B.console.clear()
		with Live(A,console=B.console,screen=True,refresh_per_second=20)as K:
			for L in range(1,101):C=L;A[E].update(J());K.update(A);time.sleep(.05)
		time.sleep(.5);B.console.clear()
	def run(A):
		'Run the module check and splash screen, and then start the main program';B=A.check_modules()
		if B:A.console.print('[bold red]Some required modules are missing![/bold red]');A.install_modules(B)
		else:A.splash_screen()