/*
 * (c)2014-2017 Forward Computing and Control Pty. Ltd.
 * NSW Australia, www.forward.com.au
 * This code is not warranted to be fit for any purpose. You may only use it at your own risk.
 * This code may be freely used for both private and commercial use
 * Provide this copyright is maintained.
 */
#include "pfodErase.h"

pfodErase::pfodErase()  {
}

void pfodErase::init(Print *_out, struct pfodDwgVALUES* _values) {
  initValues(_values);
  valuesPtr = _values;
  out = _out;
  //valuesPtr->lastDwg = this;
}

pfodErase &pfodErase::idx(uint16_t _idx) {
  valuesPtr->idx = _idx;
  return *this;
}

pfodErase &pfodErase::idx(pfodAutoIdx &a_idx) {
  idx(getAutoIdx(a_idx.idx));
  return *this;
}

pfodErase &pfodErase::cmd(const char _cmd) {
  valuesPtr->cmd = _cmd;
  valuesPtr->cmdStr = NULL;
  valuesPtr->loadCmd = ' ';
  valuesPtr->loadCmdStr = NULL;
  return *this;
}

pfodErase &pfodErase::cmd(pfodAutoCmd &a_Cmd) {
  valuesPtr->cmdStr = a_Cmd.cmd;
  valuesPtr->cmd = ' ';
  valuesPtr->loadCmd = ' ';
  valuesPtr->loadCmdStr = NULL;
  return *this;
}

pfodErase &pfodErase::cmd(const char* _cmdStr) {
  valuesPtr->cmdStr = _cmdStr;
  valuesPtr->cmd = ' ';
  valuesPtr->loadCmd = ' ';
  valuesPtr->loadCmdStr = NULL;
  return *this;
}


pfodErase &pfodErase::loadCmd(const char _loadCmd) {
  valuesPtr->loadCmd = _loadCmd;
  valuesPtr->loadCmdStr = NULL;
  valuesPtr->cmd = ' ';
  valuesPtr->cmdStr = NULL;
  return *this;
}

pfodErase &pfodErase::loadCmd(pfodAutoCmd &a_Cmd) {
  valuesPtr->loadCmd = ' ';
  valuesPtr->loadCmdStr = a_Cmd.cmd;
  valuesPtr->cmd = ' ';
  valuesPtr->cmdStr = NULL;
  return *this;
}

pfodErase &pfodErase::loadCmd(const char* _loadCmdStr) {
  valuesPtr->loadCmd = ' ';
  valuesPtr->loadCmdStr = _loadCmdStr;
  valuesPtr->cmd = ' ';
  valuesPtr->cmdStr = NULL;
  return *this;
}

// if loadCmd( ) then send 'ed' cmd else send 'e'
void pfodErase::send(char _startChar) {
  out->print(_startChar);
  if ((valuesPtr->loadCmd != ' ') || ((valuesPtr->loadCmdStr) && (*valuesPtr->loadCmdStr))) {  	  
  	out->print("ed");
    out->print('~');
    if (valuesPtr->loadCmdStr) {
      out->print(valuesPtr->loadCmdStr);
    } else {
      out->print(valuesPtr->loadCmd);
    }
  } else { 	  
    out->print('e');
    if (valuesPtr->idx > 0) {
      printIdx();
    } else {
      out->print('~');
      if ((valuesPtr->cmdStr) && (*valuesPtr->cmdStr)) {
        out->print(valuesPtr->cmdStr);
      } else {
        out->print(valuesPtr->cmd);
      }
    }
  }  
 // valuesPtr->lastDwg = NULL; // sent now
}


