#version 330

uniform vec4 color_ambient = vec4(0.1, 0.1, 0.1, 1.0);
uniform vec4 color_diffuse = vec4(0.1, 0.1, 0.1, 0.1);
uniform vec4 color_specular = vec4(1, 1, 1, 1.0);
uniform float shininess = 50.0f;

uniform vec3 light_position = vec3(6.0, 6.0, 6.0);

in vec3 position_vs;
in vec3 normal_vs;
in vec2 textures;

out vec4 color;
uniform sampler2D tex_sampler;

void main()
{
    vec3 light_direction = normalize(light_position - position_vs);
    vec3 normal = normalize(normal_vs);
    vec3 half_vector = normalize(light_direction + normalize(position_vs));
    float diffuse = max(0.0, dot(normal, light_direction));
    float specular = pow(max(0.0, dot(normal_vs, half_vector)), shininess);
    
    float ambientStrength = 0.1;

    vec4 objectColor = texture(tex_sampler, textures);
    vec4 ambient = ambientStrength * color_ambient;
    color = color_ambient + objectColor * color_diffuse + specular * color_specular;
}