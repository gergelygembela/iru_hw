#pragma once

#include "class3_1.h"
#include "class4_2.h"

class class5: public class3, public class4{
public:
    void do_something(int a) const;
};