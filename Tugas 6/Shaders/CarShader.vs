#version 330
layout(location = 0) in vec3 inposition;
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
    gl_Position = proj * view * model * vec4(inposition, 1.0f);
    
    textures = texture_cords;
    position_vs = vec3(model * vec4(inposition, 1.0f));
    normal_vs = mat3(transpose(inverse(model))) * normal;
}