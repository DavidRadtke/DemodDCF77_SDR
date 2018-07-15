
"""
DCF77_Demudulator

Dieses Programm stellt einen Signalverarbeitungsblock für das Open-Source Werkzeug "GNU-Radio" zur Anwendung und Implementierung
von Software Defined Radio dar.

Dieser Signalverarbeitungsblock hat als Input das bereits demodulierte ASK (Amplituden-Shift-Keying) Signal.
Der Signalverarbeitungsblock demoduliert nun die einzelnen Bits gibt die Uhrzeit und das Datum in der Ausgabenkonsole aus.

Autor: David Radtke
Datum: 10.07.2017

Weitere Informationen: Demodulation_DCF_77.pdf


"""

import numpy as np
from gnuradio import gr


class blk(gr.basic_block):  # basic Block -> input ungleich output


    def __init__(self, SampleDelay=1000):  
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='DCF77 Demodulator',   
            in_sig=[np.float32],
            out_sig=[np.float32],
        )


        self.SampleDelay = SampleDelay
	self.set_history(2)
	self.state=0
	self.counter=0		
	self.Bitcounter = -1   # -1, da erst bei Start einer Minute wieder 0, Zeigt aktuelles Bit
	self.Jahr = 0
	self.Monat = 0
	self.Wochentag = 0
	self.Kalendertag = 0
	self.Stunde = 0
	self.Minute = 0
	self.day = 0
    def general_work(self, input_items, output_items):
        """example: multiply with constant"""

	in0=input_items[0]
	out0=output_items[0]
	outcounter=0
	for k in range(1,len(in0)):
	
	
		if (in0[k] - in0[k-1] < 0):  				#Fallende Flanke erkannt?
			
			
			self.state=1					#state = 1, Fallende Flanke erkannt
			self.counter=self.SampleDelay			#Counter starten

		if self.state==1 and self.counter == 0:			#Status nach fallender Flanke
			
			if self.Bitcounter == 59:			#Bitcounter zurcksetzen
				self.Bitcounter = 0
			
			self.state=0

			#Logische 1 von DCF77, Start erst wenn Minute erkannt wurde (Bitcounter >= 0)
			if in0[k] == 0 and self.Bitcounter >= 0:   	
				
				# Beginn Zuweisung/Errechnen des Datums/Uhrzeit							
				if self.Bitcounter == 54:		
					self.Jahr = self.Jahr + 10 
				if self.Bitcounter == 53:
					self.Jahr = self.Jahr + 8	
				if self.Bitcounter == 52:
					self.Jahr = self.Jahr + 4
				if self.Bitcounter == 51:
					self.Jahr = self.Jahr + 2
				if self.Bitcounter == 50:
					self.Jahr = self.Jahr + 1
				if self.Bitcounter == 49:
					self.Monat = self.Monat + 10
				if self.Bitcounter == 48:
					self.Monat = self.Monat + 8
				if self.Bitcounter == 47:
					self.Monat = self.Monat + 4
				if self.Bitcounter == 46:
					self.Monat = self.Monat + 2
				if self.Bitcounter == 45:
					self.Monat = self.Monat + 1
				if self.Bitcounter == 44:
					self.Wochentag = self.Wochentag + 4
				if self.Bitcounter == 43:
					self.Wochentag = self.Wochentag + 2
				if self.Bitcounter == 42:
					self.Wochentag = self.Wochentag + 1
				if self.Bitcounter == 41:
					self.Kalendertag = self.Kalendertag + 20
 				if self.Bitcounter == 40:
					self.Kalendertag = self.Kalendertag + 10
 				if self.Bitcounter == 39:
					self.Kalendertag = self.Kalendertag + 8
 				if self.Bitcounter == 38:
					self.Kalendertag = self.Kalendertag + 4
				if self.Bitcounter == 37:
					self.Kalendertag = self.Kalendertag + 2
				if self.Bitcounter == 36:
					self.Kalendertag = self.Kalendertag + 1
				if self.Bitcounter == 34:
					self.Stunde = self.Stunde + 20
 				if self.Bitcounter == 33:
					self.Stunde = self.Stunde + 10
 				if self.Bitcounter == 32:
					self.Stunde = self.Stunde + 8
 				if self.Bitcounter == 31:
					self.Stunde = self.Stunde + 4
 				if self.Bitcounter == 30:
					self.Stunde = self.Stunde + 2
 				if self.Bitcounter == 29:
					self.Stunde = self.Stunde + 1
				if self.Bitcounter == 27:
					self.Minute = self.Minute + 40
 				if self.Bitcounter == 26:
					self.Minute = self.Minute + 20
				if self.Bitcounter == 25:
					self.Minute = self.Minute + 10			
				if self.Bitcounter == 24:
					self.Minute = self.Minute + 8
				if self.Bitcounter == 23:
					self.Minute = self.Minute + 4
				if self.Bitcounter == 22:
					self.Minute = self.Minute + 2
				if self.Bitcounter == 21:
					self.Minute = self.Minute + 1

  
 
				self.Bitcounter = self.Bitcounter + 1
				
				out0[outcounter] = 1

			if in0[k] == 1:		# logische 0 -> DCF77
				
				out0[outcounter] = 0
				self.Bitcounter = self.Bitcounter + 1
			outcounter=outcounter+1

		if self.state==0 and self.counter < -7400:  # Erstes Bit erkannt (Keine Absenkung auf 15% der Amplitude)
			
			print("Start/Stop")			
			self.counter=0
			out0[outcounter]=-1
			outcounter=outcounter+1
			self.Bitcounter = 0         # Erstes Bit

		self.counter=self.counter-1

 	self.consume(0,len(in0))
	if self.Wochentag == 1:
		self.day = 'Montag'	
	elif self.Wochentag == 2:
		self.day = 'Dienstag'
	elif self.Wochentag == 3:
		self.day = 'Mittwoch'
	elif self.Wochentag == 4:
		self.day = 'Donnerstag'
	elif self.Wochentag == 5:
		self.day = 'Freitag'
	elif self.Wochentag == 6:
		self.day = 'Samstag'
	elif self.Wochentag == 7:
		self.day = 'Sonntag'


	if self.Bitcounter == 59:		#Uhrzeit ausgeben 
		print("Zeit/Datum:  "  
  	       	 + '%0.2d' %(self.Stunde) + ":" + '%0.2d' %(self.Minute) + ",  " + str(self.day) + " der " +   
	   	'%0.2d' %(self.Kalendertag) + "." + '%0.2d' %(self.Monat) + "." + str(self.Jahr) )

		
		self.Bitcounter == -1		# Letztes Bit erreicht
	
	return outcounter
	
    

    def forecast(self, noutput_items, ninput_items_required):
        """
       forecast is only called from a general block
       this is the default implementation
       """
        ninput_items_required[0] = noutput_items	
	return
 
 
        return
