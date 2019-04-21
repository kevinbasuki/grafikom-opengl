#version 330
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texture_cords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

out vec2 textures;

void main()
{
    gl_Position =  proj * view * model * vec4(position, 1.0f);
    textures = texture_cords;
}