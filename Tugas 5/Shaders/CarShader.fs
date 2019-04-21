#version 330
in vec2 textures;

out vec4 color;
uniform sampler2D tex_sampler;

void main()
{
    float ambientStrength = 0.1;
    vec4 lightColor = vec4(1.0, 1.0, 1.0, 1.0);
    vec4 objectColor = texture(tex_sampler, textures);
    vec4 ambient = ambientStrength * lightColor;
    color = ambient * objectColor;
}