#version 330
layout(location = 0) in vec3 position;
layout(location = 1) in float opacity;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

out float opc;

void main()
{
    gl_Position =  proj * view * model * vec4(position, 1.0f);
    gl_PointSize = 4;
    opc = opacity;
}