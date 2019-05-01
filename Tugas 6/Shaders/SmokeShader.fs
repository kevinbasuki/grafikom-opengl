#version 330
layout(location = 0) out vec4 color;

in float opc;

void main()
{
    color = vec4(0.5, 0.5, 0.5, opc);
}