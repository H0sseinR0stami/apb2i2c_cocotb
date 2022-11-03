


`timescale 1ns/1ps //timescale 

module tb();
	//APB PORTS
	reg PCLK;
	reg PRESETn;
	reg [31:0] PADDR;
	reg [31:0] PWDATA;
	reg PWRITE;
	reg PSELx;
	reg PENABLE;
	wire PREADY;
	wire PSLVERR;
	wire INT_RX;
	wire INT_TX;
	wire [31:0] PRDATA;
	//I2C OUTPUT
	wire SDA_ENABLE;
	wire SCL_ENABLE;
	wire SDA;
	wire SCL;
	integer i;
	parameter integer NumberOfIputLines = 2884;  // number of lines in  "../input/apb_input.txt" file
	always  #1  PCLK = ~PCLK;
	
    reg[67:0] read_data [0:NumberOfIputLines];

	initial $readmemb("../input/apb_input.txt", read_data);
 


initial begin
PCLK =  1'b1;
	
	 
	   for (i=0; i<NumberOfIputLines; i=i+1)
        begin

            {PRESETn, PADDR, PWDATA,PWRITE,PSELx,PENABLE} = read_data[i]; @(posedge PCLK);

        end
$stop;	
end

	i2c DUT_i2c(
	//APB PORTS
	.PCLK(PCLK),
	.PRESETn(PRESETn),
	.PADDR(PADDR),
	.PWDATA(PWDATA),
	.PWRITE(PWRITE),
	.PSELx(PSELx),
	.PENABLE(PENABLE),
	.PREADY(PREADY),
	.PSLVERR(PSLVERR),
	.INT_RX(INT_RX),
	.INT_TX(INT_TX),
	.PRDATA(PRDATA),
	//I2C OUTPUT
	.SDA_ENABLE(SDA_ENABLE),
	.SCL_ENABLE(SCL_ENABLE),
	.SDA(SDA),
	.SCL(SCL)
	  );	  

`include "../properties_sva/Apb_properties.sva"

endmodule	  