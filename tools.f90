module tools

  implicit none

  type ResizableIntArray
    integer :: size = 0
    integer :: max_size = 8
    integer :: elems(8)
  end type ResizableIntArray

contains

  ! ******************************** !
  ! ResizableIntArray implementation !
  ! ******************************** !

  function get(A, idx) result(value)
    type(ResizableIntArray) :: A
    integer :: idx, value
    if (idx > A%size) then
      write(*, '(A,I0,A,I0,A)') "Trying to access element ", idx, ", but array has size ", A%size, "!"
      stop 1
    end if
    value = A%elems(idx)
  end function

  subroutine append(A, value)
    type(ResizableIntArray) :: A
    integer, allocatable :: Anew(:)
    integer :: value, i
    A%size = A%size + 1
    if (A%size > A%max_size) then
      A%max_size = 2 * A%max_size
      allocate(Anew(A%max_size))
      do i = 1, A%max_size
        Anew(i) = A%elems(i)
      end do
      A%elems = Anew
    end if
    A%elems(A%size) = value
  end subroutine

  function pop(A) result(value)
    type(ResizableIntArray) :: A
    integer :: value
    if (A%size .lt. 1) then
      write(*, *) "Trying to pop from empty array!"
      stop 1
    end if
    value = A%elems(A%size)
    A%size = A%size - 1
  end function

end module tools
