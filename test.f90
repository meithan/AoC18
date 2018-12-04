program test

  use tools
  implicit none
  integer :: i

  type(ResizableIntArray) :: A

  do i=1,10
    call append(A, i)
  end do

  write(*,*) "size=", A%size
  write(*,*) "max_size=", A%max_size
  do i=1,A%size
    write(*,*) get(A, i)
  end do

  print *, "->", get(A, 10)

  do i=1,11
    write(*,*) "pop:", pop(A)
  end do
  write(*,*) "size=", A%size
  write(*,*) "max_size=", A%max_size


end program test
