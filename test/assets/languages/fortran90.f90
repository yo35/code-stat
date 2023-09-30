! ------------------------------------------------------------------------------
! This is a file header, not counted as comment.
! ------------------------------------------------------------------------------

! I'm a comment line.

module moduleHelloWorld

	implicit none
	private
	public helloWorld

contains

	!>
	!! Say Hello! to the world.
	!!
	subroutine helloWorld()
		print *, 'Hello World!'
	end subroutine

end module

program programHelloWorld ! I'm a mixed code-comment line (counted as code).

	use moduleHelloWorld
	implicit none

	! I'm a comment line as well.
	call helloWorld()

end program
