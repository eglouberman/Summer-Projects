import Dependencies._

lazy val root = (project in file(".")).
  settings(
    inThisBuild(List(
      organization := "com.example",
      scalaVersion := "2.11.11",
      version      := "0.1.0-SNAPSHOT"
    )),
    name := "pdffigures2",
    libraryDependencies += scalaTest % Test,
    resolvers += Resolver.bintrayRepo("allenai", "maven"),
    libraryDependencies += "org.allenai" %% "pdffigures2" % "0.0.11", 
    libraryDependencies +="com.github.jai-imageio" % "jai-imageio-core" % "1.2.1",
    libraryDependencies +="com.github.jai-imageio" % "jai-imageio-jpeg2000" % "1.3.0",
    libraryDependencies += "com.levigo.jbig2" % "levigo-jbig2-imageio" % "1.6.5"
  )
