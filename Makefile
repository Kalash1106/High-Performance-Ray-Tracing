CXX = clang++
CXXFLAGS = -std=c++17 -I include -c -O3

main: main.o vec3.o color.o ray.o
	clang++ -o main main.o vec3.o color.o ray.o

main.o: src/main.cpp
	$(CXX) $(CXXFLAGS) src/main.cpp

vec3.o: src/vec3.cpp
	$(CXX) $(CXXFLAGS) src/vec3.cpp

color.o: src/color.cpp src/vec3.cpp
	$(CXX) $(CXXFLAGS) src/color.cpp

ray.o: src/ray.cpp src/vec3.cpp
	$(CXX) $(CXXFLAGS) src/ray.cpp

.PHONY: clean
clean:
	rm main *.o