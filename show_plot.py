# used to generate an html image  
from backtrader import plot
import base64
from io import BytesIO
import matplotlib
matplotlib.use("TkAgg")
    
# ...
# setup data, stratagies and broker as normal, except save the stratagies as:
# runstrats = cerebro.run() # the stratagies are returned by cerebro.run()
# ...
def getBacktestChart(runstrats):
    plotter = plot.plot.Plot(use='Agg')        
    backtestchart = ""
    for si, strat in enumerate(runstrats):
        rfig = plotter.plot(strat, figid=si * 100, numfigs=1)
        for f in rfig:
            buf = BytesIO()
            f.savefig(buf, bbox_inches='tight', format='png')
            imageSrc = base64.b64encode(buf.getvalue()).decode('ascii')
            backtestchart += f"<img src='data:image/png;base64,{imageSrc}'/>"     

    return backtestchart
