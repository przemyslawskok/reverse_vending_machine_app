#ifndef pfodCircle_h
#define pfodCircle_h
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

class pfodCircle : public pfodDwgsBase {
  public:
    pfodCircle();
    pfodCircle &radius(float _radius); // default 1
    pfodCircle &color(int _color); // default BLACK_WHITE
    pfodCircle &idx(uint16_t _idx); // default 0 i.e. not set
    pfodCircle &idx(pfodAutoIdx &a_idx); // reserve new idx if 0
    pfodCircle &filled(); // default not filled
    pfodCircle &offset(float _colOffset, float _rowOffset); // default 0,0
    void init(Print *out, struct pfodDwgVALUES* _values);
    void send(char _startChar = '|');
};
#endif // pfodCircle_h
