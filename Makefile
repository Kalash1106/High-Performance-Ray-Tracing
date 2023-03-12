CXX = clang++
CXXFLAGS = -std=c++17 -I include -c -O3 -g

main: main.o vec3.o color.o ray.o sphere.o hittable_list.o camera.o
	$(CXX) -o main main.o vec3.o color.o ray.o sphere.o hittable_list.o camera.o

main.o: src/main.cpp
	$(CXX) $(CXXFLAGS) src/main.cpp

vec3.o: src/vec3.cpp
	$(CXX) $(CXXFLAGS) src/vec3.cpp

color.o: src/color.cpp src/vec3.cpp
	$(CXX) $(CXXFLAGS) src/color.cpp

ray.o: src/ray.cpp src/vec3.cpp
	$(CXX) $(CXXFLAGS) src/ray.cpp

sphere.o: src/sphere.cpp src/vec3.cpp src/ray.cpp
	$(CXX) $(CXXFLAGS) src/sphere.cpp

hittable_list.o: src/hittable_list.cpp src/vec3.cpp src/ray.cpp
	$(CXX) $(CXXFLAGS) src/hittable_list.cpp

camera.o: src/camera.cpp src/vec3.cpp src/ray.cpp
	$(CXX) $(CXXFLAGS) src/camera.cpp


.PHONY: clean
clean:
	rm main *.o