#include "Exploder.hpp"

#include <cmath>

Exploder::Exploder(unsigned long long decayTime, int width, int height)
  : m_maxRadius{std::sqrt(width*width + height*height)}
  , m_colors(m_maxRadius + 0.5) {
}

void Exploder::setChord(const std::vector<uint8_t>& chord) {
  m_chord = chord;
}

void Exploder::tick(int type, uint8_t hue) {
  HSV hsv = {hue, 255, 255};
  m_colors.erase(m_colors.end()-1);

  if(type == -1) {
    hsv.h = m_colors[0].h;
    hsv.s = 0.9f * m_colors[0].s;
    hsv.v = 0.9f * m_colors[0].v;
  }
  else if(type == 1) {
    hsv.h = m_colors[0].h;
    hsv.s = 255;
    hsv.v = 128;
  }
  m_colors.insert(m_colors.begin(), hsv);
}

void Exploder::render(Adafruit_NeoMatrix& matrix) {
  auto curTime = millis();
  
  int width = matrix.width(), height = matrix.height();
  
  for(int x = 0; x < matrix.width(); ++x) {
    int y = height/2;
    for(int y = 0; y < matrix.height(); ++y) {
      int dx = x - width/2, dy = y - height/2;
      float r = std::sqrt(dx*dx + dy*dy);

      auto hsv = m_colors[(int)(r + 0.5f)];
      auto c = Color::HSV(hsv.h + 0.5f, hsv.s + 0.5f, hsv.v + 0.5f);
      matrix.setPixelColor(mapPixel(x, y, width, height), c.getRed(), c.getGreen(), c.getBlue());
    }
  }
}

int Exploder::mapPixel(int x, int y, int width, int height) {
  y = (x & 0x01) ? (height - y - 1) : y;

  return x*height + y;
}

