CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

all: build run

build: src/vortex_engine.cpp
	$(CXX) $(CXXFLAGS) src/vortex_engine.cpp -o vortex_engine

run: build
	./vortex_engine

clean:
	rm -f vortex_engine
