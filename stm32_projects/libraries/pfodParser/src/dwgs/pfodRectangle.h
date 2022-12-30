#ifndef pfodRectangle_h
#define pfodRectangle_h
/*
 * (c)2014-2017 Forward Computing and Control Pty. Ltd.
 * NSW Australia, www.forward.com.au
 * This code is not warranted to be fit for any purpose. You may only use it at your own risk.
 * This code may be freely used for both private and commercial use
 * Provide this copyright is maintained.
 */
#include <stdint.h>
#include <Arduino.h>
#include "pfodDwgsBase.h"

class pfodRectangle : public pfodDwgsBase {
  public:
    pfodRectangle();
    pfodRectangle &size(float width, float height); // default 1x1
    pfodRectangle &color(int _color); // default BLACK_WHITE
    pfodRectangle &idx(uint16_t _idx); // default 0 i.e. not set
    pfodRectangle &idx(pfodAutoIdx &a_idx); // reserve new idx if 0
    pfodRectangle &filled(); // default not filled
    pfodRectangle &rounded(); // default not rounded
    pfodRectangle &centered(); // default not not centered
    pfodRectangle &offset(float _colOffset, float _rowOffset); // default 0,0
    void init(Print *out, struct pfodDwgVALUES* _values);
    void send(char _startChar = '|');
};
#endif // pfodRectangle_h
