#version 330

uniform vec4 color_ambient = vec4(1.0, 1.0, 1.0, 1.0);
uniform vec4 color_diffuse = vec4(1.0, 1.0, 1.0, 1.0);
uniform vec4 color_specular = vec4(1, 1, 1, 1.0);
uniform float shininess = 50.0f;
uniform vec3 viewPos;

uniform vec3 light_position = vec3(2.0, 3.0, 4.0);

in vec3 position_vs;
in vec3 normal_vs;
in vec2 textures;

out vec4 color;
uniform sampler2D tex_sampler;

void main()
{
    vec3 light_direction = normalize(light_position - position_vs);
    vec3 normal = normalize(normal_vs);
    
    float ambientStrength = 0.1;
    vec4 ambient = ambientStrength * color_ambient;

    float diff = max(dot(normal, light_direction), 0.0);
    vec4 diffuse = diff * color_diffuse;

    float specularStrength = 1;
    vec3 viewDir = normalize(viewPos - position_vs);
    vec3 reflectDir = reflect(-light_direction, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec4 specular = specularStrength * spec * color_specular;    

    vec4 objectColor = (ambient+diffuse+specular) * texture(tex_sampler, textures);
    color = objectColor;
}