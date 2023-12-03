-- #############################################################################
-- This is a file header, not counted as comment.
-- #############################################################################

-- I'm a comment line.

CREATE FUNCTION helloWorld()
RETURNS VARCHAR(20)
BEGIN
    RETURN 'Hello World!'
END;

SELECT helloWorld(); -- I'm a mixed code-comment line (counted as code).
