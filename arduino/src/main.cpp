#include <Arduino.h>

#define str_len 32
#define separator ';'
#define terminator '\n'
#define tol 5

int motor1pin1 = 2;
int motor1pin2 = 3;

int motor2pin1 = 4;
int motor2pin2 = 5;

void setup()
{
  // put your setup code here, to run once:
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);

  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  Serial.begin(9600);
  Serial.setTimeout(100);
}

void move(double l, double r)
{
  int left = (int)(l * 255.);
  int right = (int)(r * 255.);

  bool sgnL = ((left) > 0);
  bool sgnR = ((right) > 0);

  left = abs(left);
  right = abs(right);

  if (left < tol)
  {
    analogWrite(9, 0); //ENA pin
    digitalWrite(motor1pin1, LOW);
    digitalWrite(motor1pin2, LOW);
  }
  else
  {
    if (left > 255 - tol)
      left = 255;
    analogWrite(9, left); //ENA pin
    digitalWrite(motor1pin1, sgnL);
    digitalWrite(motor1pin2, !sgnL);
  }

  if (right < tol)
  {
    analogWrite(10, 0); //ENB pin
    digitalWrite(motor2pin1, LOW);
    digitalWrite(motor2pin2, LOW);
  }
  else
  {
    if (right > 255 - tol)
      right = 255;
    analogWrite(9, right); //ENA pin
    digitalWrite(motor2pin1, sgnR);
    digitalWrite(motor2pin2, !sgnR);
  }

  //Serial.println("" + (String)left + "  " + (String)right);
}

void loop()
{
  char str[str_len];
  char left_s[str_len];
  char right_s[str_len];
  str[0] = '\0';
  left_s[0] = '\0';
  right_s[0] = '\0';

  int i = 0;
  while (true)
  {
    int code = Serial.read();
    if (code == -1)
    {
      delay(1);
      continue;
    }
    char c = (char)code;
    if (c == terminator)
    {
      str[i] = '\0';
      i = 0;

      int len = strlen(str);
      char *pointer = strchr(str, separator);

      if (len < 3)
        continue;
      if (pointer == NULL)
        continue;

      int index = (int)(pointer - str);

      strncpy(left_s, str, index);
      strncpy(right_s, pointer + 1, len - index);

      double left = strtod(left_s, NULL);
      double right = strtod(right_s, NULL);

      move(left, right);
    }
    str[i] = c;
    i++;
    if (i >= str_len)
      i = 0;
  }
}