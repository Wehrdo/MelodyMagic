#pragma once

#include <vector>

#include <Adafruit_NeoMatrix.h>

class Twinkler {
public:
  Twinkler(unsigned long long fadeTime, int width, int height);

  void addTwinkle(uint8_t hue);

  void render(Adafruit_NeoMatrix& matrix);

private:
  struct Twinkle {
    unsigned long long startTime;
    int x, y;
    uint8_t hue;
  };

  unsigned long long m_fadeTime;
  int m_width, m_height;
  std::vector<Twinkle> m_twinkles;
};

