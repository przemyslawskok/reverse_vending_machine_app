/*
  Timebase callback
  This example shows how to configure HardwareTimer to execute a callback at regular interval.
  Callback toggles pin.
  Once configured, there is only CPU load for callbacks executions.
*/

#if !defined(STM32_CORE_VERSION) || (STM32_CORE_VERSION  < 0x01090000)
#error "Due to API change, this sketch is compatible with STM32_CORE_VERSION  >= 0x01090000"
#endif

#if defined(LED_BUILTIN)
#define pin  LED_BUILTIN
#else
#define pin  D2
#endif

void Update_IT_callback(void)
{ // Toggle pin. 10hz toogle --> 5Hz PWM
  digitalWrite(pin, !digitalRead(pin));
}


void setup()
{
#if defined(TIM1)
  TIM_TypeDef *Instance = TIM1;
#else
  TIM_TypeDef *Instance = TIM2;
#endif

  // Instantiate HardwareTimer object. Thanks to 'new' instanciation, HardwareTimer is not destructed when setup() function is finished.
  HardwareTimer *MyTim = new HardwareTimer(Instance);

  // configure pin in output mode
  pinMode(pin, OUTPUT);

  MyTim->setOverflow(10, HERTZ_FORMAT); // 10 Hz
  MyTim->attachInterrupt(Update_IT_callback);
  MyTim->resume();
}


void loop()
{
  /* Nothing to do all is done by hardware. Even no interrupt required. */
}