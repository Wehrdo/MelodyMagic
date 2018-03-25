#pragma once

#include <vector>
#include <Adafruit_NeoMatrix.h>

#include "Color.hpp"

class Exploder {
public:
  struct HSV {
    float h, s, v;
  };

  Exploder(unsigned long long decayTime, int width, int height);

  void setChord(const std::vector<uint8_t>& chord);

  void tick(int type = -1, uint8_t hue = 0);

  void render(Adafruit_NeoMatrix& matrix);

  static int mapPixel(int x, int y, int width, int height);

private:
  Color getColor(unsigned long long curTime, double r) const;

  double m_maxRadius;
  std::vector<uint8_t> m_chord;
  std::vector<HSV> m_colors;
};

