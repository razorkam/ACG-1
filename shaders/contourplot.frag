#version 330 core
in vec3 vFragPosition;
in vec2 vTexCoords;
in vec3 vNormal;

out vec4 color;

uniform sampler2D tex;

void main()
{
  vec3 pos = vFragPosition;
  vec3 lightDir = vec3(1.0f, 1.0f, 0.0f);
  float f = pos.y/15.0;
  float s = 6*f;
  float r = max(0, (3 - f*abs(s-4)- f*abs(s-5))/2);
  float g = max(0, (4 - f*abs(s-2)- f*abs(s-4))/2);
  float b = max(0, (3 - f*abs(s-1)- f*abs(s-2))/2);
  vec3 col = vec3(1-r,1-g,1-b); //vec3(0.0f, 0.9f, 0.75f);

  float kd = max(dot(vNormal, lightDir), 0.0);

  color = vec4(kd * col, 1.0f);
}