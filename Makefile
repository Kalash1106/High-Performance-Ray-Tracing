CXX = clang++
CXXFLAGS = -std=c++17 -I include -c -O3

main: main.o vec3.o color.o
	clang++ -o main main.o vec3.o color.o

main.o: src/main.cpp
	$(CXX) $(CXXFLAGS) src/main.cpp

vec3.o: src/vec3.cpp
	$(CXX) $(CXXFLAGS) src/vec3.cpp

color.o: src/color.cpp src/vec3.cpp
	$(CXX) $(CXXFLAGS) src/color.cpp

.PHONY: clean
clean:
	rm main *.o