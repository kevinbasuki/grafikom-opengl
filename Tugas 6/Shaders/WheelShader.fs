#version 330
layout(location = 0) out vec4 color;

void main()
{
	float ambientStrength = 0.1;
    vec4 lightColor = vec4(1.0, 1.0, 1.0, 1.0);
    vec4 objectColor = vec4(0.0, 0.0, 0.0, 1.0);
    vec4 ambient = ambientStrength * lightColor;
    color = ambient * objectColor;
}