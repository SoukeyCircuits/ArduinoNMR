June 2026 Update and Explainer:

To do list: 
	
  -Upload Accessory PCB files
	
  -Add alternative attenuator and LNA.
	
  -Upload control code
	
  -Add Arduino Giga Display + display software
	
  -Show preliminary results from working device
	
  -Add non JLC BOM (Mouser, Aliexpress, etc)
	
  -Add raspberry pi multiple instrument control software.
  
The main sections of the Arduino NMR are the RF synthesis, RF input, and the Tayloe detector. 

RF synthesis begins with the SI5351A-B-GM chip connected to an ABM8G-25.000MHZ-4Y-T3, a  25 MHz crystal oscillator. The 20QFN package for the SI5351 was specifically chosen over the 16QFN as it was having issues with the Etherkit SI5351 library and not indexing the clock outputs correctly. The SI5351A-B-GM is still unable to use CLK6 and CLK7 as they are handled differently from CLK0-CLK5. Although it would be possible to control all 8 outputs, the function is sufficient for the design as is. The primary output clocks CLK0-CLK3 are connected to an ADG904BRUZ in an SP4T configuration. The switch allows for indexing either 0°, 90°, 180°, and 270° phase for a single frequency or 0° and a second phase at two separate frequencies. 

The output is then fed into a PE4251MLI-Z SPDT switch. Since both single and dual frequency setups have an available channel containing the 0° at the Larmor frequency, when not transmitting, the channel can be used for Homodyne demodulation. Alternatively, one of the clocks can be set to a secondary offset frequency for Heterodyne demodulation. 

When actively transmitting, the output is sent through a PE43650 attenuator for digital control of the RF power output. Although the PE43650 was chosen based on availability and price, it would be advantageous to include the PE43711B-Z as an option in the future. The PE43650 has 0.5 dB step sizes with a maximum attenuation of 15.5 dB, but an improvement with the PE43711B-Z would give 0.25 dB step sizes and a maximum attenuation of 31.5 dB. For these applications, 0.5 dB is sufficient and maximum power can be limited by an external attenuator on the output(s).

fter attenuation, the final stage is either a bridged solder jumper, or another PE4251MLI-Z SPDT switch. This switch is what controls the two TX output options. Each output will need its own external attenuator to limit the maximum power output as well as a filter. The SI5351 only emits a square shaped output and harmonic frequencies must be filtered out for a pure sinusoidal output at the desired frequency. This allows for connecting a single spectrometer to multiple instruments each with their own dedicated TX and RX ports.

After amplification, further accessory parts are available for filtering, conditioning, and pulse breakthrough limitation. All of these accessories fit inside a 50x25x25mm aluminum enclosure available on Aliexpress but require drilling holes for the SMA connectors. The first accessory is the LC filter. This design is able to fit a 7 pole LC filter within the small enclosure for high off frequency rejection for both ≤100W and ≤5W depending on which side is populated. 

Another accompanying accessory is the crossed-diode duplexer to reject low power noise from the amplifier while passing the high powered pulse. By populating the diodes at the top of the design and not populating the lower diodes, this gives a path of 3 pairs of crossed diodes before reaching the center SMA port leading to the magnet. By changing the diodes populated to the bottom half of the board, bridging the top solder jumper, and not including the center SMA header, the same board can be used for crossed diodes to ground. It should be said, never try to combine these two functions as they are for separate uses and it could damage your equipment.

When attempting to capture the NMR signal, always filter before the signal enters the RX ports. Like with the TX ports, the signal can either go into the default solder bridged SMA connector, or be actively switched between the two RX ports. Once the signal has entered the RX portion of the board, there is one additional PE4251MLI-Z SPDT switch to protect the preamplifier from the pulse breakthrough. This switch is normally closed to a 50 Ω terminator but can be GPIO controlled to open after the desired deadtime. When open, the signal passes into a multiple stage low noise amplifier (LNA). The LNA is a dual stage PHA-13HLN+ amplifier with approximately 48-51 dB of gain with a noise figure ≤3. An additional design with budget conscience in mind alternatively uses a dual GALI-S66+ design for $10 instead of $30. This design has a smaller 42 dB gain and has a similar noise figure above 10 MHz but the noise figure skyrockets below 10 MHz. 

After the preamplifier, the design has one of two options for configuration, bridging the triple solder pad to the left, sends the signal directly into the Tayloe detector. Alternatively, bridging the solder to the right and additionally at the end allows for additional filtering after the LNA. If RX1 and RX2 are close in frequency, the filter can be set to cut off just at the frequency of interest. If the desire is for wide band operation from 1-100 MHz, it is advised to still filter the 100+ MHz frequency as both LNAs have additional noise at or above that frequency. The performance of the LNA and accompanying filtering can be measured by disconnecting C43, not powering the 5V line, and connecting to the center SMA connector as the output. It is advised to validate the gain and noise figure of the LNA prior to connecting to the SN74LV4052ADR. 

Once the signal is amplified and filtered, the signal will pass through the C43 DC blocking capacitor and enter a DC offset of 1.66V using a 3.3V voltage splitter. The signal will then enter the SN74LV4052ADR setup in the configuration of a Tayloe detector inspired by the ESP32 designed https://github.com/thaaraak. As a brief overview, by mixing the 0° and 90° signals from the SI5351 into the SN74LV4052ADR A & B pins and our amplified signal into the COM port, we are able to split the IF into their 0°, 90°, 180°, and 270° components. By then connecting the 0° to the positive end and 180° into the negative end of an operational amplifier, the in-phase signal is the resulting output and can be measured. By repeating with the 90° and 270° components, the quadrature signal can also be acquired. 

Finally, the I/Q signal is measured using the Arduino Giga’s built in ADC pins. Since the clock frequency of the Arduino Giga is 480 MHz, the ADC is capable of measuring up to 12.5 Msps for each channel. This uses the https://github.com/Bexin3/STMSpeeduino as a starting point but uses my built in pulse control software to handle the timing. 
