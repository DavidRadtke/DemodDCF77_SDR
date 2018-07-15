"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Differentiator',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.set_history(1000)
     
 
    def work(self, input_items, output_items):
		x = 'idle'
		in0 = input_items[0]
		out0 = output_items[0]
		for k in range(0,len(out0)):
			if (in0[k+1] - in0[k] == 1):  # flanke nach oben
				
                        	print('high')
				out0[k] = 1
				x = 'high' 
			elif (in0[k+1] - in0[k] < 0): # flanke nach unten
								
				out0[k] = -1
				print('low')
				x = 'low'
			elif (in0[k+1] - in0[k] == 0): # idle
				out0[k] = 0
			
				
	        return len(output_items[0])
