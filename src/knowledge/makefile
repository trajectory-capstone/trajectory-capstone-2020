PATH_ROOT := ../..

RM := rm -f

all: 	
	@echo 'Compiling the knowledge construction example...\n';
	g++ -I$(PATH_ROOT) -Wall -c -DDEBUG -O0 -o "main.o" main.cpp;
	g++ -L$(PATH_ROOT)/lib -o"main" ./main.o -lLPM;
	@echo '\nDone';
  
clean:	
	@echo 'Cleaning...\n';
	-$(RM) main.o main;
	@echo '\nDone';
