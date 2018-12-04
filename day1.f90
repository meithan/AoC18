program day1

  implicit none
  integer, parameter :: N = 973
  integer :: iostatus, inc, i, j, s, freq
  integer, dimension(N) :: increments
  integer, dimension(140000) :: seen
  logical :: found

  open(unit=99, file="day1.in", status='old')
  do i=1,N
    read(99, *) inc
    increments(i) = inc
  end do

  ! Part 1
  freq = 0
  do i=1,N
    freq = freq + increments(i)
  end do
  write(*,*) "Part 1: ", freq

  ! Part 2
  s = 0
  freq = 0
  found = .false.
  i = 1
  do
    freq = freq + increments(i)
    do j=1,s
      ! write(*,*) seen(j), freq
      if (seen(j) .eq. freq) then
        found = .true.
      end if
    end do
    s = s + 1
    ! write(*,*) s
    seen(s) = freq
    if (found) then
      exit
    end if
    i = i + 1
    if (i > N) then
      i = 1
    end if
  end do
  write(*,*) "Part 2: ", freq

end program
