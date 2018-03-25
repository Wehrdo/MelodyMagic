#include "Twinkler.hpp"

#include "Exploder.hpp"
#include "Color.hpp"

Twinkler::Twinkler(unsigned long long fadeTime, int width, int height)
  : m_fadeTime{fadeTime}
  , m_width{width}
  , m_height{height} {
}

void Twinkler::addTwinkle(uint8_t hue) {
  int x = rand() % m_width, y = rand() % m_height;
  m_twinkles.push_back({millis(), x, y, hue});
}

void Twinkler::render(Adafruit_NeoMatrix& matrix) {
  auto curTime = millis();

  for(int i = 0; i < m_twinkles.size(); ++i) {
    unsigned long long dt = curTime - m_twinkles[i].startTime;
    if(dt >= m_fadeTime) {
      m_twinkles.erase(m_twinkles.begin() + i);
      --i;
    }
    else {
      uint8_t brightness = 255 * (m_fadeTime - dt) / m_fadeTime;
      uint8_t radius = 4 * dt / m_fadeTime;
      auto c = Color::HSV(m_twinkles[i].hue, 255, brightness);
      /*
      matrix.setPixelColor(Exploder::mapPixel(m_twinkles[i].x, m_twinkles[i].y, m_width, m_height),
        c.getRed(), c.getGreen(), c.getBlue());
      */
      matrix.drawCircle(m_twinkles[i].x, m_twinkles[i].y, radius,
        matrix.Color(c.getRed(), c.getGreen(), c.getBlue()));
    }
  }
}

