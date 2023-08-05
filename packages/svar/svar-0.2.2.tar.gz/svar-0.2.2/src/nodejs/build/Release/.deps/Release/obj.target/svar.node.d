cmd_Release/obj.target/svar.node := g++ -shared -pthread -rdynamic -m64  -Wl,-soname=svar.node -o Release/obj.target/svar.node -Wl,--start-group Release/obj.target/svar/src/main.o -Wl,--end-group 
