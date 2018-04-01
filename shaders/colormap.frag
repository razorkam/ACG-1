#version 330 core
in vec3 vFragPosition;
in vec2 vTexCoords;
in vec3 vNormal;

out vec4 color;

uniform sampler2D tex;


vec4 colormap1(float f)
{
    f = clamp( f, 0.0, 1.0 );
    return vec4(1.0, f, 1.0 - f, 1.0);
}

void main()
{
  vec3 lightDir = vec3(1.0f, 1.0f, 0.0f);

  vec3 sampled = texture(tex, vTexCoords).rgb;
  float grayscale = 0.299f*sampled.r + 0.587f*sampled.g + 0.114*sampled.b;

//  vec4 col = colormap1( grayscale );

  vec4 col = vec4( sampled, 1.0f );

  float kd = max(dot(vNormal, lightDir), 0.0);

  color = kd * col;
}