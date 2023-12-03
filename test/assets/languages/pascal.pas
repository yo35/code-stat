(******************************************************************************
 * This is a file header, not counted as comment.                             *
 ******************************************************************************)

// I'm a comment line.
{$hint I'm a compiler directive (counted as code). }

program programHelloWorld;

{ Say Hello! to the world. }
procedure helloWorld;
begin
    writeln('Hello World!')
end;

begin // I'm a mixed code-comment line (counted as code).

    // I'm a comment line as well.
    helloWorld()

    { I'm a comment block
    spanning several lines. }

end.
