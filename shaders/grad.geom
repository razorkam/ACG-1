#version 330 core
layout (lines) in;
layout (line_strip, max_vertices = 2) out;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = gl_in[0].gl_Position ;
    EmitVertex();

    gl_Position = gl_in[1].gl_Position ;
    EmitVertex();

    gl_Position = gl_in[1].gl_Position - vec4(view)/100 ;
    EmitVertex();
//
//    gl_Position = gl_in[1].gl_Position;
//    EmitVertex();
//
//    gl_Position = gl_in[1].gl_Position + vec4(view)/5  ;
//    EmitVertex();



    EndPrimitive();
}
