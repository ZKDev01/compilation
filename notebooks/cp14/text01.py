text = """
class A {
  a : int ;
  def suma ( a : int , b : int ) : int {
    a + b ;
  }
  b : int ;
}

class B : A {
  c : A ;
  def f ( d : int , a : A ) : void {
    let f : int = 8 ;
    let c = new A ( ) . suma ( 5 , f ) ;
    c ;
  }
}
"""