#version 330 core
layout(location = 0) in vec3 vertex;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 texCoords;


out vec2 vTexCoords;
out vec3 vFragPosition;
out vec3 vNormal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform sampler2D tex;

void main()
{
  vec3 pos = vertex;
  gl_Position = projection * view * model * vec4(vertex, 1.0f);
  pos.y += 3.0f * texture(tex, texCoords).r;
  gl_Position = projection * view * model * vec4(pos, 1.0f);
  
  vTexCoords = texCoords;
  vFragPosition = vec3(model * vec4(vertex, 1.0f));
  vNormal = mat3(transpose(inverse(model))) * normal;
}