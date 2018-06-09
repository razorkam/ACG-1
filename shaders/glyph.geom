#version 330 core
layout (points) in;
layout (line_strip, max_vertices = 5) out;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = vec4(projection * view * model * vec4(0.0,0.0,0.0,1.0));
    EmitVertex();

    gl_Position = gl_in[0].gl_Position - vec4(projection * view * model * vec4(0.0,0.0,0.0,1.0))/5;
    EmitVertex();

    gl_Position = gl_in[0].gl_Position - vec4(projection * view * model * vec4(0.0,0.0,0.0,1.0))/5 + vec4(1.0,0.0,0.0,1.0);
    EmitVertex();

    gl_Position = gl_in[0].gl_Position - vec4(projection * view * model * vec4(0.0,0.0,0.0,1.0))/5;
    EmitVertex();

    gl_Position = gl_in[0].gl_Position - vec4(projection * view * model * vec4(0.0,0.0,0.0,1.0))/5 + vec4(-1.0,0.0,0.0,1.0);
    EmitVertex();




    EndPrimitive();
}
