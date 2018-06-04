#version 330 core
layout(location = 0) in vec3 vertex;
layout(location = 1) in vec3 normal;
//layout(location = 2) in vec2 texCoords;


//out vec2 vTexCoords;
out vec3 vFragPosition;
out vec3 vNormal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform sampler2D tex;

void main()
{

  gl_Position = projection * view * model * vec4(vertex, 1.0f);
  vFragPosition = vertex; // pass raw vertex coords to compite vector field parameters in fragment shader
  vNormal = mat3(transpose(inverse(model))) * normal;
}