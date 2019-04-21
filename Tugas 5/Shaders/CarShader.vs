#version 330
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texture_cords;
layout(location = 2) in vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

out vec2 textures;
out vec3 position_vs;
out vec3 normal_vs;

void main()
{
    vec4 position = proj * view * model * vec4(position, 1.0f);
    gl_Position =  position;

    textures = texture_cords;
    position_vs = position.xyz;
    normal_vs = normal;
}